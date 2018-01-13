运行环境：
linux
tensorflow>=v1.2.0
sonnet

运行方法：
1.进入tools目录运行./compile_tools.sh
2.把附件的slt_arctic拷贝到egs目录下，tools拷贝到本目录下。
3.进入egs/slt_arctic目录运行./run_tts.sh可以跑blstm模型，运行./run_SOL.sh可以跑论文提出的BLSTM_SOL模型。
3.实现的论文代码主要在 src/models/tf_model_SOL.py中。
