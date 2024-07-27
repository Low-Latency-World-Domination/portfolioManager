build:
	python -m grpc_tools.protoc -Isp_proto/ --python_out=./sp --pyi_out=./sp --grpc_python_out=./sp ./sp_proto/*.proto
	touch sp/__init__.py
	
