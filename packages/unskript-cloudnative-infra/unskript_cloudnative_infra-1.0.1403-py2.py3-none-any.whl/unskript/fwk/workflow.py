#
# Copyright (c) 2021 unSkript.com
# All rights reserved.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE
#
#
from __future__ import annotations

import json
import sys
import traceback

from polling2 import poll
from unskript import connectors
from unskript.legos.utils import CheckOutput, CheckOutputStatus
from unskript.schemas.credentials import ConnectorEnum
from unskript.connectors.infra import InfraConnector
from unskript.secrets import ENV_MODE, SECRET_STORE_TYPE
from unskript.fwk.cellparams import TaskParams, eval_with_try
from unskript.fwk.iter import IterCfg, PollCfg
from unskript.schemas.conditions import TaskStartConditionSchema
from json import loads as json_loads
from typing import Tuple
from jsonschema import ValidationError
from beartype.roar import BeartypeCallHintPepParamException
from unskript.schemas.credentials import TaskCredentialValueSchema
from typing import List

import collections.abc

# Wrapper around Lamdba function
def lambda_wrapper(lego_callback, hdr, **args):
    try:
        result_from_lambda = lego_callback(hdr, **args)
        return result_from_lambda
    except Exception as e:
        raise e



def singleton(class_):
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance

@singleton
class Workflow():

    env = None
    secrets_store = None
    params = None
    user = None
    catch_exceptions = False
    done = False
    tasks = {}
    global_vars = {}
    task_output = {}
    output_params = {} #Capture the values for the output parameters of the runbook.

    def __init__(self, env, secrets_store_cfg, params, uuid=None, catch_exceptions=False, global_vars=None, check_uuids: List[str]=None):
        self.env = env
        self.secrets_store = connectors.SecretStoreApi(
            env[ENV_MODE], secrets_store_cfg[SECRET_STORE_TYPE], secrets_store_cfg)
        self.params = params
        self.user = None  # TBD: RBAC
        self.check_uuids = check_uuids
        # For checks run, we want to ignore exceptions as each cell will be a single check and we want all the cells to finish running.
        if check_uuids is not None:
            self.catch_exceptions = True
            self.check_run = True
        else:
            self.catch_exceptions = catch_exceptions
            self.check_run = False
        self.uuid = uuid
        if global_vars is not None:
            self.global_vars = global_vars
        # check_output is a map of checks output, with key being the uuid of the check and value being the Checkoutput object.
        self.check_output = {}
        self.task_index = 0
        self.output_params = {}
        self.cached_cloud_handles = {}
        self.cached_credential_types = [
                    ConnectorEnum.aws,
                    ConnectorEnum.azure,
                    ConnectorEnum.k8s,
                    ConnectorEnum.gcp
                    ]
        return None

    def increment_task_index(self):
        self.task_index = self.task_index + 1

    def print_tasks(self):
        for task in self.tasks:
            task.print()

    def Done(self, rc):

        # TBD: we should connect with the user interface here and turn off the run button
        # or else bring down the kernel if there is such an API
        # For now, we just skip over all cells, but there is code outside of the framework
        # it will end up getting executed.
        self.done = True
        self.rc = rc
        return

    def get_workflow_uuid(self):
        return self.uuid

    def get_cached_credential_types(self):
        return self.cached_credential_types

    def get_handle(self, workflow):
        handle = InfraConnector().get_handle(workflow=workflow)
        return handle

    def get_task_index(self):
        return self.task_index

    # set_output sets the value of the output parameter of the runbook.
    # It takes the output parameter name and its value as input.
    # It checks if the output parameter is already defined in the globals, throws an exception if it isnt.
    def set_output(self, output_parameter_name:str, output_parameter_value: any):
        #Check if the output parameter exists in the global vars
        allGlobalVariables = self.global_vars.keys()
        if output_parameter_name not in allGlobalVariables:
            raise Exception(f'Output parameter {output_parameter_name} not defined. Please add the output parameter by clicking on Parameters button')

        self.output_params[output_parameter_name] = self.global_vars.get(output_parameter_value)
        self.global_vars.update({output_parameter_name: self.output_params[output_parameter_name]})

    def get_cached_credential(self, credential_type: ConnectorEnum):
        if credential_type not in self.get_cached_credential_types():
            return None
        return self.cached_cloud_handles.get(credential_type, None)

    def put_cached_credential(self, credential_type: ConnectorEnum, handle):
        self.cached_cloud_handles[credential_type] = handle
        return


# this is pure for now, but it should ideally be wrapping the legos
class Action():

    def __init__(self) -> None:
        pass

    def validate(self, schema, params, iter_item=None, vars=None, inputIsJson=True):
        # Input param validation.
        inputParams = TaskParams(schema, params, iter_item, vars, inputIsJson)
        return (None, inputParams.get_params_kwargs())


class Task():

    display_fields = [
        "iter_config_str",
        "conditions_config_str",
        "credentials_config_str",
        "legoSchema",
        "inputParamsJson",
        "poll_config_str",
        "name",
        "output"
    ]

    def __init__(self, w: Workflow, name: str = None):
        # configuration items
        self.task_index = w.get_task_index()
        w.increment_task_index()
        self.workflow = w

        self.v = {}
        self.v.update(globals())
        self.iter_config_str = None
        self.conditions_config_str = None
        self.credentials_config_str = None
        self.legoSchema = None
        self.inputParamsJson = None
        self.poll_config_str = None
        self.output_name = None
        self.print_output = True
        self.continue_on_error = False
        self.name = name
        # status items
        self.output = None
        self.num_iterated = 0
        self.skipped_execution = False

        self.args_iter = []
        self.iter_result = {}
        self.iter_passed = 0
        self.iter_failed = 0

        # Add custom exception hook, this will


        pass

    def print(self):
        for p, v in vars(self).items():
            if p in Task.display_fields:
                print(f"{p}: {v}")

    def set_task_name(self, name):
        if name != None:
            self.name = name

    def configure(self, inputParamsJson: str = None, credentialsJson: str = None,
                        iterJson: str = None, conditionsJson: str = None, pollJson: str = None,
                        outputName: str = None, printOutput: bool = None, continueOnError: bool = None):
        if iterJson is not None:
            self.iter_config_str = iterJson.strip()

        if conditionsJson is not None:
            self.conditions_config_str = conditionsJson

        if credentialsJson is not None:
            self.credentials_config_str = credentialsJson

        if inputParamsJson is not None:
            self.inputParamsJson = inputParamsJson

        if pollJson is not None:
            self.poll_config_str = pollJson

        if outputName is not None:
            self.output_name = outputName

        if printOutput is not None:
            self.print_output = printOutput

        if continueOnError is not None:
            self.continue_on_error = continueOnError


    def validate_iter(self, handle, legoSchema):
        if self.iter_config.getIterListIsConstant():
            iterObject = self.iter_config.getIterListValue()
        else:
            iterObject = eval_with_try(self.iter_config.getIterListName(), self.v)

        args_iter = list()
        for item in iterObject:
            (err, args) = Action().validate(
                legoSchema, self.inputParamsJson, item, self.v)
            if err is not None:
                return (err, None, None)
            self.args_iter.append(item)
            list.append(args_iter, args)

        return (None, handle, args_iter)

    # lookup based on service_id and credential_type and return the ID
    # NB: this only works for non-docker mode
    def get_credential_id(self, connectorObject):
        infra_handle = self.workflow.get_handle(workflow=self.workflow)
        key = self.workflow.env.get('TENANT_ID') + ":" + \
                self.workflow.env.get('PROXY_ID') + ":" + \
                self.workflow.global_vars.get('environment') + ":" + \
                connectorObject.credential_service_id + ":" + \
                connectorObject.credential_type
        value = infra_handle.get_workflow_key(key)
        if not value:
            raise Exception("Credential not found for the Environment %s and " \
                            "ServiceID %s" % (self.workflow.global_vars.get('environment'), \
                            connectorObject.credential_service_id))

        credential_id = value.decode("utf-8") if value else ""
        return credential_id

    def validate(self, legoSchema=None, vars: dict() = None, infra: bool = False, inputIsJson: bool = True):

        if self.credentials_config_str is None and infra is False:
            print("Error: Credential not selected")
            return (ValueError, None, None)

        # legoSchema = None
        self.v.update(vars)
        self.iter_config = IterCfg(self.iter_config_str)
        try:
            if infra is True:
                handle = self.workflow.get_handle(workflow=self.workflow)
            else:
                credentials_config = json_loads(self.credentials_config_str)
                connectorObject = TaskCredentialValueSchema(**credentials_config)

                if connectorObject.credential_name is not None: #By Credential Name
                    handle = self.workflow.secrets_store.get_handle(
                        self.credentials_config_str)

                    # cache it as needed in workflow
                    if handle != None:
                        self.workflow.put_cached_credential(
                            connectorObject.credential_type, handle)

                elif connectorObject.credential_service_id is not None: #By Service ID
                    if not self.workflow.global_vars.get('environment'):
                        raise Exception("Service ID based selection is not supported for this runbook since its not running in an Environment")

                    credentials_config['credential_id'] = self.get_credential_id(connectorObject)
                    handle = self.workflow.secrets_store.get_handle(json.dumps((credentials_config)))

                else:
                    # Try the workflow cache By Credential Type
                    handle = self.workflow.get_cached_credential(connectorObject.credential_type)
                    print("Unspecified credential: using cached global credential from workflow")
                    if handle is None:
                        # try to load default configs
                        # this works only for AWS and k8s
                        # if the file $HOME/.kube/config exists, then load it
                        if connectorObject.credential_type in self.workflow.get_cached_credential_types():
                            import os
                            if os.path.exists(os.path.expanduser("~/.kube/config")):

                                handle = self.workflow.secrets_store.get_handle(
                                    json.dumps({"credential_type": "CONNECTOR_TYPE_K8S"}), True)

                        if handle == None:
                            raise Exception("Invalid credential configuration")
                        else:
                            # cache it as needed in workflow
                            self.workflow.put_cached_credential(
                                connectorObject.credential_type, handle)

        except Exception as e:
            print(f"Error in obtaining credential: {e}")
            return (e, None, None)

        self.poll_config = PollCfg(self.poll_config_str)

        # validate params
        args = None
        try:
            if self.iter_config.getIterEnabled() is True:
                return self.validate_iter(handle, legoSchema)
            elif self.poll_config.getPollEnabled() is True:
                (err, args) = Action().validate(
                    legoSchema, self.inputParamsJson, vars=self.v)
                return (err, handle, args)
            else:
                (err, args) = Action().validate(
                    legoSchema, self.inputParamsJson, vars=self.v, inputIsJson=inputIsJson)
                return (err, handle, args)
        except Exception as e:
            print(f'Error in validating input: {e}')
            if self.workflow.catch_exceptions is False:
                raise e
            return (e, None, None)

    def parse_conditions(self):

        if self.conditions_config_str == None:
            return False

        # parse the conditionsCfg JSON
        d = json_loads(self.conditions_config_str)
        try:
            self.conditions = TaskStartConditionSchema(**d)
        except ValidationError as e:
            return False

        return self.conditions.condition_enabled

    def evaluate_conditions(self, args):
        # evaluate conditions
        return (eval(self.conditions.condition_cfg, self.v) == self.conditions.condition_result)

    def evaluate_poll(self, lego_callback, hdl, args):
        poll_forever = self.poll_config.getPollTimeout() == None

        if self.poll_config.getPollCheckIsValue() is False:
            print("Non-value type poll not yet implemented")
            return None


        if self.poll_config.getPollCheckValueBool() is not None:
            poll_config = self.poll_config.getPollCheckValueBool()

        elif self.poll_config.getPollCheckValueInt() is not None:
            poll_config = self.poll_config.getPollCheckValueInt()

        elif self.poll_config.getPollCheckValueStr() is not None:
            poll_config = self.poll_config.getPollCheckValueStr()

        # else:
        #     # poll check is an expression
        #     res = poll(lambda: lego_callback(hdl, **args), self.poll_config.getPollStepInterval(),
        #         check_success=(lambda x: x == eval(self.poll_config.getPollConditionCfg(), self.v)),
        #         timeout=self.poll_config.getPollTimeout())

        poll_config = eval(str(poll_config), self.v)
        res = poll(lambda: lambda_wrapper(lego_callback, hdl, **args), self.poll_config.getPollStepInterval(),
                       check_success=(lambda x: x == poll_config),
                       timeout=self.poll_config.getPollTimeout(), poll_forever=poll_forever)
        return res

    def execute_worker(self, lego_callback, hdl, args):
        res = None
        self.name = str(lego_callback).split()[1]

        # workflow is explicitly marked done. Don't execute any more steps
        # Attention: this has to be the first step and should not be moved down
        if self.workflow.done:
            return None

        # reset unskript_task_error and unskript_failed_keys
        try:
            self.workflow.global_vars.update({'unskript_task_error': None})
            self.workflow.global_vars.update({'unskript_failed_keys': {}})
        except:
            # Not to worry, it may not be set
            pass

        # skip if start condition is configured and evaluated to false
        try:
            if self.parse_conditions() == True and self.evaluate_conditions(args) == False:
                print("\nSkipping invocation since start condition(",
                    self.conditions.condition_cfg, ") is enabled and did not pass")
                self.skipped_execution = True
                return None
        except Exception as e:
                print(f"\nException Occurred while evaluating the start condition: {e}")
                return None

        try:
            if self.iter_config.getIterEnabled():
                # Construct a Map having key as iter_tem and value as return value of the function
                res = {}
                err = {}
                idx = 0
                for arg in args:
                    if arg is None:
                        continue
                    self.num_iterated = self.num_iterated + 1
                    # Check if args_iter is hashable
                    try:
                        from collections import Hashable
                    except:
                        from collections.abc import Hashable

                    if isinstance(self.args_iter[idx], Hashable) == True:
                        # Hashable
                        pass
                    else:
                        # Not Hashable
                        self.args_iter[idx] = str(self.args_iter[idx])

                    try:
                        lres = lego_callback(hdl, **arg)
                        # Handle Duplicate Key scenario
                        if self.args_iter[idx] not in res:
                            res[self.args_iter[idx]] = lres
                        elif isinstance(res[self.args_iter[idx]], list):
                            print("WARNING: Duplicate Entry found in the Iterator Value")
                            res[self.args_iter[idx]].append(lres)
                        else:
                            print("WARNING: Duplicate Entry found in the Iterator Value")
                            res[self.args_iter[idx]] = [res[self.args_iter[idx]], lres]

                        self.iter_result[self.args_iter[idx]] = u'\u2713'
                        self.iter_passed = self.iter_passed + 1
                    except Exception as e:
                        self.iter_result[self.args_iter[idx]] = u'\u2717'
                        self.iter_failed = self.iter_failed + 1
                        if self.workflow.global_vars is not None:
                            self.workflow.global_vars.update({'unskript_task_error': e.__str__()})
                            self.workflow.global_vars.update({'unskript_failed_keys': err})
                        if self.continue_on_error == True:
                            err[self.args_iter[idx]] = f"An Error occurred while executing: {e}"
                        else:
                            err[self.args_iter[idx]] = f"An Exception occured. Halting execution {e}"
                            break

                    idx = idx + 1

            elif self.poll_config.getPollEnabled():
                res = self.evaluate_poll(lego_callback, hdl, args)

            else:
                # single invocation
                try:
                    if args is None:
                        res = lego_callback(hdl)
                    else:
                        res = lego_callback(hdl, **args)
                except Exception as e:
                    if self.workflow.global_vars is not None:
                        self.workflow.global_vars.update({'unskript_task_error': e.__str__()})
                    raise e

        except BeartypeCallHintPepParamException as e:
            #For check run, we need to show the exact error that happened, so all exceptions should be sent as it is.
            if self.workflow.check_run:
                raise e
            print(f"Error: Parameter type validation failed: {e}")
            return None

        except ValueError as e:
            if self.workflow.check_run:
                raise e
            print(f"Error: Parameter value error: {e}")
            return None

        except TypeError as e:
            if self.workflow.check_run:
                raise e
            print(f"Error: Parameter type validation failed: {e}")
            return None

        except NameError as e:
            if self.workflow.check_run:
                raise e
            print(f"Error: Parameter name validation failed: {e}")
            return None

        except Exception as e:
            print(f"Error while executing: {e}")
            raise e

        return res

    # Execute returns a Tuple of Output of the Lego
    # And any error if it encountered
    # For checks run, we should capture the output returned from the checks and store it inside the Workflow object.
    # This way, we can do the print of that field in the last cell and thats how we can show the return values from checks.
    # Also for checks run, since we want the runbook to finish, we should ignore any cell exception.
    def execute(self, lego_callback, hdl, args, lego_printer=None):
        check_output = CheckOutput(status=CheckOutputStatus.SUCCESS)
        try:
            self.output = self.execute_worker(lego_callback, hdl, args)
            retval = (self.output, '')
            if self.workflow.global_vars != None:
                if self.output_name != None \
                    and self.workflow.global_vars['unskript_task_error'] is None \
                    and self.skipped_execution == False:
                        self.workflow.global_vars.update({self.output_name: self.output})

            if self.iter_config.getIterEnabled():
                print("Execution Summary: ")
                print(f"   Number of Execution(s): {self.num_iterated}")

            if self.workflow.check_run:
                if self.task_index >= len(self.workflow.check_uuids):
                    print(f'Invalid task_index {self.task_index}, check_uuids len {len(self.workflow.check_uuids)}')
                    return retval
                # If the output is not a tuple, raise an exception
                if isinstance(self.output, Tuple) == False:
                    raise Exception(f'Checks output should be a Tuple')

                if self.output[0] == True:
                    check_output.status = CheckOutputStatus.SUCCESS
                else:
                    check_output.status = CheckOutputStatus.FAILED
                check_output.objects = self.output[1]
            elif self.print_output == True:
                if self.output is not None:
                    if self.iter_config.getIterEnabled():
                        print("   Iterator values:")
                        for elem in self.args_iter:
                            try:
                                from collections import Hashable
                            except:
                                from collections.abc import Hashable
                            if isinstance(elem, Hashable) == True:
                                pass
                            else:
                                elem = str(elem)
                            if elem in self.iter_result:
                                print(f"        {elem}\t\t: {self.iter_result[elem]}")
                    else:
                        if lego_printer is not None:
                            try:
                                lego_printer(self.output)
                            except:
                                # Lego Printer is not implemented
                                pass
            else:
                if self.iter_config.getIterEnabled():
                    print("   Passed Iteration(s): ", u'\u2713', self.iter_passed, '..')
                    print("   Failed Iteration(s): ", u'\u2717', self.iter_failed, '..')
                else:
                    print("Task Executed")

        except Exception as e:
            self.output = None
            retval = (self.output, str(e.__str__()))

            if self.workflow.global_vars['unskript_task_error'] is not None:
                print(f"Execution Failed: Error: {self.workflow.global_vars['unskript_task_error']}")
                print(f"  Task Parameters: {args}")
                if self.workflow.global_vars['unskript_failed_keys'] is not {}:
                    for key in self.workflow.global_vars['unskript_failed_keys']:
                        print(f"\t {key} \t: {self.workflow.global_vars['unskript_failed_keys'][key]}")

            if self.workflow.check_run:
                # Look up check uuid for the task index
                if self.task_index >= len(self.workflow.check_uuids):
                    print(f'Invalid task_index {self.task_index}, check_uuids len {len(self.workflow.check_uuids)}')
                    return retval
                check_output.status = CheckOutputStatus.RUN_EXCEPTION
                check_output.error = str(e)

            if self.workflow.catch_exceptions is False:
                raise e

        if self.workflow.check_run:
            self.workflow.check_output[self.workflow.check_uuids[self.task_index]] = check_output.json()
            retval = check_output

        return retval

