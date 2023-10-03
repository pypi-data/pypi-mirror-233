#!/usr/bin/env python
"""
Launch a transformation from CWL workflow descriptions

Usage:
    cta-prod-submit-from-cwl <name of the Transformation> <type of the Transformation> <path of the directory containing CWL files> <optional: dataset name> <optional: group_size>

Examples:
    cta-prod-submit-from-cwl Transformation_test MCSimulation ../CWL
    cta-prod-submit-from-cwl Transformation_test Processing ../CWL Prod5b_LaPalma_AdvancedBaseline_NSB1x_electron_North_20deg_R1 5
"""

__RCSID__ = "$Id$"

from DIRAC.Core.Base.Script import Script
from CTADIRAC.Interfaces.API.MCPipeNSBJob import MCPipeNSBJob
from CTADIRAC.Interfaces.API.CtapipeProcessJob import CtapipeProcessJob
from CTADIRAC.Core.Utilities.tool_box import get_dataset_MQ

import DIRAC
from DIRAC.TransformationSystem.Client.Transformation import Transformation
from cwltool.load_tool import load_tool
from cwltool.context import LoadingContext, RuntimeContext
import cwltool.process
import cwltool.main
import schema_salad
import shellescape
import re
import copy
import os


class WorkflowStep:
    """Composite class for workflow step (production step + job)"""

    #############################################################################

    def __init__(self):
        """Constructor"""
        self.command_line = ""

    def get_command_line(self, input_cwl, input_yaml):
        """Get command line from a CommandLineTool description"""

        loader = schema_salad.ref_resolver.Loader(
            {"@base": input_yaml, "path": {"@type": "@id"}}
        )
        inputs, _ = loader.resolve_ref(input_yaml)

        for entry in inputs.values():
            if check_if_file_input(entry):
                add_fake_file(entry["location"])

        loading_context = LoadingContext({"strict": False, "debug": True})
        step = load_tool(input_cwl, loading_context)
        for inp in step.tool["inputs"]:
            if cwltool.process.shortname(inp["id"]) in inputs:
                pass
            elif (
                cwltool.process.shortname(inp["id"]) not in inputs and "default" in inp
            ):
                inputs[cwltool.process.shortname(inp["id"])] = copy.copy(inp["default"])
            elif (
                cwltool.process.shortname(inp["id"]) not in inputs
                and inp["type"][0] == "null"
            ):
                pass
            else:
                raise Exception(
                    f"Missing inputs `{cwltool.process.shortname(inp['id'])}`"
                )

        runtime_context = RuntimeContext()

        for job in step.job(inputs, None, runtime_context):
            for i in range(len(job.builder.bindings)):
                if isinstance(
                    job.builder.bindings[i]["datum"], dict
                ):  # replace file path by its location
                    if "location" in job.builder.bindings[i]["datum"]:
                        path = job.builder.bindings[i]["datum"]["path"]
                        location = job.builder.bindings[i]["datum"]["location"]
                        for k in range(len(job.command_line)):
                            if path in job.command_line[k]:
                                job.command_line[k] = job.command_line[k].replace(
                                    path, location
                                )
            self.command_line = " ".join([maybe_quote(arg) for arg in job.command_line])

        for entry in inputs.values():
            if check_if_file_input(entry):
                remove_fake_file(entry["location"])
        return


def check_if_file_input(entry):
    if isinstance(entry, dict):
        if "class" in entry:
            if entry["class"] == "File":
                return True
    else:
        return False


def add_fake_file(location):
    dir = os.path.dirname(location)
    if dir != "":
        if not os.path.exists(dir):
            os.makedirs(dir)
    open(location, "a").close()
    return


def remove_fake_file(location):
    os.remove(location)
    return


def maybe_quote(arg):
    needs_shell_quoting = re.compile(r"""(^$|[\s|&;()<>\'"$@])""").search
    return shellescape.quote(arg) if needs_shell_quoting(arg) else arg


def submit_simulation_transformation(
    transfo, transfo_name, setup_cwl, setup_yml, run_cwl, run_yml, data_cwl, data_yml
):
    """Build MC Simulation Transformation"""

    # Build Transformation
    transfo.Name = "MCSimulation"
    transfo.setTransformationName(transfo_name)  # this must be unique
    transfo.setType("MCSimulation")
    transfo.setDescription("Prod6 MC Pipe TS")
    transfo.setLongDescription("Prod6 simulation pipeline")  # mandatory

    # Build WorkflowSteps
    step1 = WorkflowStep()
    step1.get_command_line(setup_cwl, setup_yml)

    step2 = WorkflowStep()
    step2.get_command_line(run_cwl, run_yml)
    step2.command_line = (
        "./" + step2.command_line
    )  # add ./ since dirac_prod_run is not a command

    step3 = WorkflowStep()
    step3.get_command_line(data_cwl, data_yml)

    # Build Job
    MCJob = MCPipeNSBJob()
    MCJob.setType("MCSimulation")
    MCJob.setOutputSandbox(["*Log.txt"])

    # Replace static run number with dynamic run number to run with DIRAC
    step2.command_line = re.sub(
        "--run [0-9]+", f"--run {MCJob.run_number}", step2.command_line
    )

    # Run workflow
    i_step = 1
    sw_step = MCJob.setExecutable(
        str(step1.command_line.split(" ", 1)[0]),
        arguments=str(step1.command_line.split(" ", 1)[1]),
        logFile="SetupSoftware_Log.txt",
    )
    sw_step["Value"]["name"] = "Step%i_SetupSoftware" % i_step
    sw_step["Value"]["descr_short"] = "Setup software"
    i_step += 1

    cs_step = MCJob.setExecutable(
        str(step2.command_line.split(" ", 1)[0]),
        arguments=str(step2.command_line.split(" ", 1)[1]),
        logFile="CorsikaSimtel_Log.txt",
    )

    cs_step["Value"]["name"] = "Step%i_CorsikaSimtel" % i_step
    cs_step["Value"]["descr_short"] = "Run Corsika piped into simtel"

    i_step += 1
    dm_step = MCJob.setExecutable(
        str(step3.command_line.split(" ", 1)[0]),
        arguments=str(step3.command_line.split(" ", 1)[1]),
        logFile="DataManagement_dark_Log.txt",
    )

    dm_step["Value"]["name"] = f"Step{i_step}_DataManagement"
    dm_step["Value"]["descr_short"] = "Save data files to SE and register them in DFC"

    MCJob.setExecutionEnv({"NSHOW": "10"})

    # Submit Transformation
    transfo.setBody(MCJob.workflow.toXML())
    result = transfo.addTransformation()  # transformation is created here
    if not result["OK"]:
        return result
    transfo.setStatus("Active")
    transfo.setAgentType("Automatic")
    return result


def submit_processing_transformation(
    transfo,
    transfo_name,
    dataset,
    group_size,
    setup_cwl,
    setup_yml,
    run_cwl,
    run_yml,
    data_cwl,
    data_yml,
):
    """Build Processing Transformation"""

    # Build Transformation
    transfo.Name = "Prod5_ctapipe_processing"
    transfo.setTransformationName(transfo_name)  # this must be unique
    transfo.setType("DataReprocessing")
    transfo.setDescription("ctapipe Modeling TS")
    transfo.setLongDescription("ctapipe Modeling processing")  # mandatory

    # Build WorkflowSteps
    step1 = WorkflowStep()
    step1.get_command_line(setup_cwl, setup_yml)

    step2 = WorkflowStep()
    step2.get_command_line(run_cwl, run_yml)
    step2.command_line = (
        "./" + step2.command_line
    )  # add ./ since dirac_ctapipe-process_wrapper is not a command

    step3 = WorkflowStep()
    step3.get_command_line(data_cwl, data_yml)

    input_meta_query = get_dataset_MQ(dataset)

    # Build Job
    ProcessingJob = CtapipeProcessJob(cpuTime=259200.0)
    ProcessingJob.setOutputSandbox(["*Log.txt"])

    # Run workflow
    i_step = 1
    sw_step = ProcessingJob.setExecutable(
        str(step1.command_line.split(" ", 1)[0]),
        arguments=str(step1.command_line.split(" ", 1)[1]),
        logFile="SetupSoftware_Log.txt",
    )
    sw_step["Value"]["name"] = "Step%i_SetupSoftware" % i_step
    sw_step["Value"]["descr_short"] = "Setup software"
    i_step += 1

    cs_step = ProcessingJob.setExecutable(
        str(step2.command_line.split(" ", 1)[0]),
        arguments=str(step2.command_line.split(" ", 1)[1]),
        logFile="ctapipe_stage1_Log.txt",
    )

    cs_step["Value"]["name"] = "Step%i_ctapipe_stage1" % i_step
    cs_step["Value"]["descr_short"] = "Run ctapipe stage 1"

    i_step += 1
    dm_step = ProcessingJob.setExecutable(
        str(step3.command_line.split(" ", 1)[0]),
        arguments=str(step3.command_line.split(" ", 1)[1]),
        logFile="DataManagement_Log.txt",
    )

    dm_step["Value"]["name"] = f"Step{i_step}_DataManagement"
    dm_step["Value"]["descr_short"] = "Save data files to SE and register them in DFC"

    # Submit Transformation
    transfo.setBody(ProcessingJob.workflow.toXML())
    transfo.setGroupSize(group_size)
    transfo.setInputMetaQuery(input_meta_query)
    result = transfo.addTransformation()  # transformation is created here
    if not result["OK"]:
        return result
    transfo.setStatus("Active")
    transfo.setAgentType("Automatic")
    return result


@Script()
def main():
    Script.parseCommandLine()
    argss = Script.getPositionalArgs()
    if len(argss) not in [3, 5]:
        Script.showHelp()
    transfo_name = argss[0]
    type = argss[1]
    config_dir = argss[2]
    if len(argss) >= 4:
        dataset = argss[3]
        if len(argss) == 5:
            group_size = int(argss[4])
    if type.lower() == "mcsimulation":
        transfo = Transformation()
        setup_cwl = os.path.join(config_dir, "setup-software.cwl")
        setup_yml = os.path.join(config_dir, "setup-software.yml")
        run_cwl = os.path.join(config_dir, "dirac_prod_run.cwl")
        run_yml = os.path.join(config_dir, "dirac_prod_run.yml")
        data_cwl = os.path.join(config_dir, "cta-user-managedata.cwl")
        data_yml = os.path.join(config_dir, "cta-user-managedata.yml")
        result = submit_simulation_transformation(
            transfo,
            transfo_name,
            setup_cwl,
            setup_yml,
            run_cwl,
            run_yml,
            data_cwl,
            data_yml,
        )
    elif type.lower() == "processing":
        transfo = Transformation()
        setup_cwl = os.path.join(config_dir, "setup-software.cwl")
        setup_yml = os.path.join(config_dir, "setup-software-processing.yml")
        run_cwl = os.path.join(config_dir, "dirac_ctapipe-process_wrapper.cwl")
        run_yml = os.path.join(config_dir, "dirac_ctapipe-process_wrapper.yml")
        data_cwl = os.path.join(config_dir, "cta-user-managedata.cwl")
        data_yml = os.path.join(config_dir, "cta-user-managedata-processing.yml")
        result = submit_processing_transformation(
            transfo,
            transfo_name,
            dataset,
            group_size,
            setup_cwl,
            setup_yml,
            run_cwl,
            run_yml,
            data_cwl,
            data_yml,
        )
    try:
        if not result["OK"]:
            DIRAC.gLogger.error(result["Message"])
            DIRAC.exit(-1)
        else:
            DIRAC.gLogger.notice("Done")
    except Exception:
        DIRAC.gLogger.exception()
        DIRAC.exit(-1)


if __name__ == "__main__":
    main()
