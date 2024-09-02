build:
	python -m grpc_tools.protoc -Isp_proto/ --python_out=. --pyi_out=. --grpc_python_out=. ./sp_proto/*.proto
	touch sp/__init__.py
	
evans:
	cd sp_proto && evans --proto portfolio_manager.proto -p 50052
