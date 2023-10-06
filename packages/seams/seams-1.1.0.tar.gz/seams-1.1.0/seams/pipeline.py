from seams import Seams
from abc import ABC, abstractmethod
import os
import tempfile
import json
import time
import calendar
import datetime
import argparse
import sys
import csv
from seams.severity import Severity
from traceback import format_tb
from dotenv import load_dotenv

# The default path and name of the log file
SEAMS_PIPELINE_LOG_FILE = "pipeline.log" 

load_dotenv()
class Pipeline(ABC):
    

    def __init__( self, 
                  SECRET:str = None,
                  APP_ID: str = None, 
                  TENANT_ID: str = None, 
                  URL:str = None, 
                  AD_AUTH_MODE:str = None ):
        '''
        Create an instance of the Pipeline interface
        '''

        if SECRET is None:
            SECRET = os.getenv("AD_APP_SECRET")
        if APP_ID is None:
            APP_ID = os.getenv("AD_APP_ID")
        if TENANT_ID is None:
            TENANT_ID = os.getenv("AD_TENANT_ID")
        if URL is None:
            URL = os.getenv("API_URL")
        if AD_AUTH_MODE is None:
            AD_AUTH_MODE = os.getenv("AD_AUTH_MODE")

        self.result_files = []
        self.logs = "pipeline_logs.csv"
        self.user_logs = "pipeline_user_logs.csv"
        self.__prep_log_files()
        self.secret = SECRET
        self.seams = Seams(URL)

        self.seams.connect(SECRET, APP_ID, TENANT_ID, AD_AUTH_MODE)

        self.log_file = open(SEAMS_PIPELINE_LOG_FILE, "w")


    def __prep_log_files(self):
        '''
        opens the log files and writes the headers
        '''
        index = ["severity", "date", "message"]
        with open(self.logs, "w", newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=index)
            writer.writeheader()
        with open(self.user_logs, "w", newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=index)
            writer.writeheader()

    
    @abstractmethod
    def run(self, 
            data:dict = None) -> None:
        '''

        Abstract class that will be overwritten by the user.

        *** Extend the Pipeline class and create a run method ***

        '''
        print("ERROR: this method should be overridden")


    def start(self) -> None:
        '''
        starts a pipeline and does all the buildup and tear down for every pipeline

        :returns:
            JSON object representing the status of the completed pipeline
        '''

        error = False

        try:

            #getting parameters and setting them to appropriate class variables
            parameters = self.__get_parameters()
            self.vertex_id = parameters["vertex_id"]
            self.schema_id = parameters["tenant_id"]

            #setting pipeline status to IN PROGRESS
            self.update_pipeline_status_in_progress() 

            #getting the run parameters of pipeline
            data = json.loads(self.seams.get_vertex_by_id(self.vertex_id)["runParameters"])

            if "Files" in data:
                #downloading files
                self.log_info( "verifying files...")
                self.__verify_files(data)
                self.log_info("downloading files...")
                data["files"] = self.download_input_files()

            #running abstract run method
            self.run(data)

        except BaseException as e:
 
            error = True
            #if pipeline fails setting pipeline to ERROR and printing out the stack trace
            etype, value, tb = sys.exc_info()
 
            #formats the exception type into a string and grabs only the class type of the error
            exception_type = str(type(value)).replace("'", "").split(" ")[1][:-1]
            self.log_error(format_tb(tb))
            self.log_error(exception_type, ": ", str(value).replace("'", ""), for_user=True)
 
        finally:
            if error:
                return self.update_pipeline_status_error()
            else:
                return self.update_pipeline_status_done()

            self.log_file.close()


    def __verify_files(self, 
                       data:dict) -> None:
        '''
        Verifies that the files coming into the pipeline aren't already attached to the Pipeline

        This method assures that pipelines can run again without attaching duplicate files.
        '''

        curr_input_files = self.seams.get_edge_vertices(self.vertex_id, "PipelineInputFile", "out")["vertices"]
        
        vertex_list = []
        name_list = []

        for item in curr_input_files:
            matching_files = [curr_data["vertexId"] for curr_data in data["Files"] if curr_data["vertexId"] == item["id"]]
            if len(matching_files) > 0:
                vertex_list.append(matching_files[0])
            matching_files = [curr_data["name"] for curr_data in data["Files"] if curr_data["name"] == item["name"]]
            if len(matching_files) > 0:
                name_list.append(matching_files[0])

        for item in data["Files"]:
            if item["vertexId"] not in vertex_list and item["name"] not in name_list:
                self.seams.attach_edges(self.vertex_id, [item['vertexId']])


    def update_pipeline_status_in_progress(self) -> str:
        '''
        sets the pipeline status to IN PROGRESS

        :returns:
            JSON object representing the status of the completed pipeline
        '''

        attributes = {
            "status": "IN PROGRESS"
        }

        return self.seams.update_vertex(self.vertex_id, "PipelineRun", attributes)
    

    def update_pipeline_status_done(self) -> str:
        '''
        sets the pipeline status to DONE

        :returns:
            JSON object representing the status of the completed pipeline
        '''

        upload_log_files = self.__build_log_upload_files()
        attributes = {
            "status": "DONE",
            "runResults": self.result_files,
            "logs": upload_log_files[0],
            "userLogs": upload_log_files[1]
        }

        return self.seams.update_vertex(self.vertex_id, "PipelineRun", attributes)
        

    def update_pipeline_status_error(self) -> str:
        '''
        sets the pipeline status to ERROR

        :returns:
            JSON object representing the status of the completed pipeline
        '''

        upload_log_files = self.__build_log_upload_files()
        attributes = {
            "status": "ERROR",
            "runResults": self.result_files,
            "logs": upload_log_files[0],
            "userLogs": upload_log_files[1]
        }

        return self.seams.update_vertex(self.vertex_id, "PipelineRun", attributes)


    def download_input_files(self) -> list:
        '''
        downloads any files needed by the pipeline

        :returns:
            list of file paths for files downloaded for the pipeline
        '''

        files = []
        curr_input_files = self.seams.get_edge_vertices(self.vertex_id, "PipelineInputFile", "out")["vertices"]

        #downloads files in pipeline, adds them to a temp file, adds file path to a list
        for item in curr_input_files:
            download = self.seams.download_file(item["id"])
            files.append(download)

        return files
    

    def get_result_files(self) -> list:
        '''
        returns a list of all files created by the pipeline

        :returns:
            list of all files created by the pipelie
        '''
        return self.result_files


    def add_result_file(self, file_vertex_id:str, label:str, name:str) -> None:
        '''
        adds a new result file to the result files list

        '''
        new_file = {
            "id": file_vertex_id,
            "label": label, 
            "name": name
        }
        self.result_files.append(new_file)
    

    def get_schema_id(self) -> str:
        '''
        Returns SEAMS schema id
        '''
        return self.schema_id
    

    def __write_to_log(self, 
                       log_file:dict = None, 
                       line:dict = None):
        '''
        This is a private function that will do all the work of opening a log file and writing to it
        '''
        index = ["severity", "date", "message"]
        with open(log_file, "a", newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=index)
            writer.writerow(line)
        csvfile.close()
        
        # file.close()


    def log(self, log_severity:str, 
            *args:list, 
            for_user:bool = False, 
            print_out:bool = True) -> None:
        '''
        logs any stdout or stderr and saves it to the pipeline run vertex

        :param log_severity:
            The severity of the log, severity will be verified by the Severity class  **REQUIRED**
        :param *args:
            Comma delimited list of anything the user wishes to print out  **REQUIRED**
        :param for_user:
            False by default, if set to True will send the log to userLogs
        '''
        #gets UTC time
        date = datetime.datetime.now(datetime.timezone.utc)
        result = ""
        #check if severity exists
        temp_args = args
        if isinstance(log_severity, Severity):
            for arg in temp_args:
                if isinstance(arg, list):
                    #checks if each item is a dict
                    temp = ""
                    if isinstance(arg[0], dict):
                        for item in arg:
                            temp = temp + json.dumps(item) + ", "
                        temp = temp.rstrip(temp[-2:])
                        result = result + "[" + "".join(temp) + "]"
                    else:
                        result = result + " ".join(arg)
                elif isinstance(arg, dict):
                    result = result + json.dumps(arg)
                else:
                    result = result + str(arg)

            #creating log object
            log = {
                "severity": log_severity.name,
                "date": str(date),
                "message": result
            }

            #builds readable string and prints it out
            str_log = "{:8} {} - {}".format(log["severity"], date, log["message"])
            if print_out:
                print(str_log)
                self.log_file.write(str_log + "\n")

            #appends to logs and user_logs if requested
            self.__write_to_log(self.logs, log)
            if for_user:
                self.__write_to_log(self.user_logs, log)


    def log_info(self, *args, for_user=False, print_out=True) -> None:
        """
        Wrapper method for logging info severity messages
        """
        self.log(Severity.INFO, *args, for_user=for_user, print_out=print_out)

    def log_error(self, *args, for_user=False, print_out=True) -> None:
        """
        Wrapper method for logging error severity messages
        """
        self.log(Severity.ERROR, *args, for_user=for_user, print_out=print_out)

    def log_debug(self, *args, for_user=False, print_out=True) -> None:
        """
        Wrapper method for logging debug severity messages
        """
        self.log(Severity.DEBUG, *args, for_user=for_user, print_out=print_out)

    def log_critical(self, *args, for_user=False, print_out=True) -> None:
        """
        Wrapper method for logging critical severity messages
        """
        self.log(Severity.CRITICAL, *args, for_user=for_user, print_out=print_out)

    def log_success(self, *args, for_user=False, print_out=True) -> None:
        """
        Wrapper method for logging success severity messages
        """
        self.log(Severity.SUCCESS, *args, for_user=for_user, print_out=print_out)

    def log_warning(self, *args, for_user=False, print_out=True) -> None:
        """
        Wrapper method for logging warning severity messages
        """
        self.log(Severity.WARNING, *args, for_user=for_user, print_out=print_out)


    def create_new_file(self,
                        filename: str) -> tuple[str, str]:
        """Creates a new tempfile and returns the filepath

        Returns tuple with filepath and filename of new file

        """

        i = 0
        split_name = filename.split(".")
        new_filename = ""

        for item in split_name:
            if i == len(split_name)-1:
                new_filename = new_filename + "_" + str(datetime.datetime.now()) + "." + item
            else:
                new_filename = new_filename + "." + item
            i+=1
        new_filename = new_filename.replace(" ", "_").replace(":", ".").lstrip(".")
        upload_file_path = os.path.join(tempfile.gettempdir(), new_filename)

        return upload_file_path, new_filename


    def __build_log_upload_files(self) -> tuple[str, str]:
        '''
        private method to build and upload log files

        :returns:
            (vertex_id of log file, vertex_id of user_log file)
        '''

        #uploads log file and attaches it as an edge to the pipeline run
        log_file_upload = self.seams.upload_file("logs for {}".format(self.vertex_id), self.logs, file_type="PipelineLogFile")
        self.seams.attach_edges(self.vertex_id, [ log_file_upload["id"] ])

        #uploads user_log file and attaches it as an edge to the pipeline run
        user_log_file_upload = self.seams.upload_file("user logs for {}".format(self.vertex_id), self.user_logs, file_type="PipelineLogFile")
        self.seams.attach_edges(self.vertex_id, [user_log_file_upload["id"]])

        return (log_file_upload["id"], user_log_file_upload["id"])

    
    def __check_int(self, 
                    value:str):
        try:
            return int(value)
        except:
            return value


    def __get_parameters(self) -> dict:
        '''
        private method to get the parameters in a pipeline

        :returns:
            dict of all the command line arguments sent to the pipeline
        '''

        parser = argparse.ArgumentParser()
        parser.add_argument("--schemaId",
                            help="Schema ID of the pipeline job, call with --schemaId")
        parser.add_argument("--pipelineRunId", nargs="?",
                            help="Pipeline Run ID of the pipeline job, call with --pipelineRunId")
        parser.add_argument("--pipelineName", nargs="?",
                            help="Name of the pipeline job, call with --pipelineName")
        parser.add_argument("--pipelineId", nargs="?",
                            help="Id of the pipeline job, call with --pipelineId")

        args = parser.parse_args()
        if not args.schemaId:
            parser.error(
                "Schema Id required - do -h for help")

        # Set the default SEAMS schema
        self.seams.set_current_schema_by_id(self.__check_int(args.schemaId))

        pipeline_run_vertex_id = ""
        if args.pipelineName and args.pipelineId:
            pipeline_run_submit_time = str(int((time.mktime(datetime.datetime.now().timetuple())))) + "000"

            attributes = {
                "dateSubmitted": pipeline_run_submit_time,
                "status": "SUBMITTED",
                "runParameters": '{"Initializer": "Scheduled"}',
                "runResults": '[]',
                "pipelineId": args.pipelineId,
                "pipeLineName": args.pipelineName
            }

            pipeline_name = args.pipelineName.lower().replace(" ", "-") + "-" + pipeline_run_submit_time

            self.log(Severity.INFO, "No pipeline run vertex id found, creating a new one with the following attributes: ", attributes)

            new_pipeline_run = self.seams.create_vertex("PipelineRun", pipeline_name, attributes)
            pipeline_run_vertex_id = new_pipeline_run["id"]

        else:
            pipeline_run_vertex_id = args.pipelineRunId

        parameters = {"tenant_id": args.schemaId, "vertex_id": pipeline_run_vertex_id}
        return parameters


