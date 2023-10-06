# from fastapi import FastAPI, Path
# from pydantic import BaseModel
# from singulr_client.singulrtracergenerator import SingulrTracerGenerator
# from typing import Dict, Any, Optional
# from run import Run
# import time
# import uvicorn
# import pandas as pd
# import json
#
# st = SingulrTracerGenerator()
#
#
# class RunCreate(BaseModel):
#     name: str
#     inputs: Dict[str, Any]
#     run_type: str
#     execution_order: Optional[int] = None
#     session_name: str
#
#
# class RunUpdate(BaseModel):
#     # Define the fields you want to update here.
#     # For example, if you want to update 'name' and 'inputs':
#     name: Optional[str] = None
#     inputs: Optional[Dict[str, Any]] = None
#
#
#
# def create_run(run_data: Run):
#     # Your create_run logic here
#     # Access run_data.name, run_data.inputs, run_data.run_type, etc.
#     # Access project_name if provided as a query parameter
#     run_data = json.dumps(json.loads(run_data))
#
#     #print("creating run id entry in database: {}".format(Run.dict(run_data)))
#     file_name = str(run_data["id"]) + "-" + str(int(time.time()))
#     st.start_trace(run_data)
#     df = pd.DataFrame.from_dict([run_data])
#     df = df.astype(str)
#     df.to_parquet("~/Downloads/traces/create_event/{}.parquet".format(file_name), engine='pyarrow')
#     return {"message": "Run created successfully"}
#
#
# def update_run(run_id: str, run_data: Run):
#     # Your update_run logic here
#     # Access run_id and run_data to perform the update
#     run_data = json.loads(run_data)
#     print("updating run id entry in database{}".format(run_id))
#     # print("updating run data {}".format(Run.dict(run_data)))
#     file_name = str(run_data.id) + "-" + str(int(time.time()))
#     st.end_trace(run_data)
#     df = pd.DataFrame.from_dict([run_data.dict()])
#     df = df.astype(str)
#     df.to_parquet("~/Downloads/traces/update_event/{}.parquet".format(file_name), engine='pyarrow')
#     return {"message": f"Run {run_id} updated successfully"}
#
#
# def get_run(run_id: str = Path(..., description="The ID of the run")):
#     # Your get_run logic here
#     # Access run_id to retrieve the run
#     print("acçessing run_id {}".format(run_id))
#     return {"message": f"Run {run_id} retrieved successfully"}
#
#
#
# if __name__ == '__main__':
#     uvicorn.run(app, host="0.0.0.0", port=8001)
