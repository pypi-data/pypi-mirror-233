from wonkaai.Chat import ChatFunction
from wonkaai.ResultAnalyser import ResultAnalyser
import json

class ChatFunctionMultiple(ChatFunction):

    def __init__(self, prompt_template, n=10, **kwargs):
        super().__init__(prompt_template, n=n, **kwargs)

    def generate(self, function_schema=..., no_error=True, **kwargs):
        response = super().generate(function_schema, no_error, **kwargs)

        if response == "ERROR":
            return {"error" : "ERROR"}
        
        if response.get("choices") is None:
            return {"error" : "ERROR"}
        
        choices = response.get("choices")

        result_analyser = ResultAnalyser()
        arguments = []
        for choice in choices :
            message = choice.get("message")
            if message is None :
                result_analyser.add_result({"error" : "no message"})
                continue
            function_call = message.get("function_call")
            if function_call is None :
                result_analyser.add_result({"error" : "no function call"})
                continue   
            name = function_call.get("name")
            arguments =  function_call.get("arguments")
            if name is None or arguments is None :
                result_analyser.add_result({"error" : "no function name"})
                continue
            if name != function_schema[0]["name"] :
                result_analyser.add_result({"error" : "invalid function name"})
                continue
            if arguments is None :
                result_analyser.add_result({"error" : "no function arguments"})
                continue

            try :
                result_analyser.add_result(json.loads(arguments))
            except :
                result_analyser.add_result({"error" : "invalid json"})
                continue
        result_analyser.analyse()
        return result_analyser
                    
    
        
