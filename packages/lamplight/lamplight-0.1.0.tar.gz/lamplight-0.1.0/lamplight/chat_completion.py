
import json
from typing import Callable, List, Optional, Union
from pydantic import BaseModel, Field, create_model, validator
from pydantic.fields import FieldInfo
import openai
from rich import print


class FunctionCall(BaseModel):
    name: str = Field(description="The name of the function to be called.")
    arguments: str = Field("{}", description="The arguments for the function call.")


class Message(BaseModel):
    role: str = Field(description="The role of the message author.")
    content: Optional[str] = Field(None, description="The contents of the message.")
    name: Optional[str] = Field(
        None, description="The name of the author of this message."
    )
    function_call: Optional[FunctionCall] = Field(
        None, description="The name and arguments of a function that should be called."
    )

    @validator('content', pre=True)
    def content_none_to_str(cls, v):
        if v is None:
            return ''
        return v

    @classmethod
    def from_response(cls, response) -> "Message":
        return cls(**response.choices[0].message)


class Function(BaseModel):
    name: str = Field(description="The name of the function.")
    description: Optional[str] = Field(
        None, description="A description of what the function does."
    )
    parameters: dict = Field(
        description="The parameters the function accepts, described as a JSON Schema object."
    )

    callable: Callable = Field(exclude=True)
    auto_execute: bool = Field(exclude=True)

    @classmethod
    def from_annotated_function(cls, func: Callable, auto=True) -> "Function":
        """
        Convert a function with annotated fields into a Function BaseModel
        """
        parameters = {}
        for parameter_name, parameter_type in func.__annotations__.items():
            if parameter_name != "return":
                field_default = Field()
                if func.__defaults__ is not None:
                    field_default = func.__defaults__[
                        func.__code__.co_varnames.index(parameter_name)
                    ]

                if isinstance(field_default, FieldInfo):
                    parameters[parameter_name] = (parameter_type, field_default)

        parameters = {
            "type": "object",
            "properties": create_model(func.__name__, **parameters).schema()[
                "properties"
            ],
        }
        return cls(
            callable=func,
            auto_execute=auto,
            name=func.__name__,
            description=func.__doc__,
            parameters=parameters,
        )


class Chat(BaseModel):
    model: str = Field(
        default="gpt-4",
        description="ID of the model to use. See the model endpoint compatibility table for details on which models work with the Chat API.",
    )
    messages: List[Message] = Field(
        default_factory=list,
        description="A list of messages comprising the conversation so far.",
    )
    functions: List[Function] = Field(
        default_factory=list,
        description="A list of functions the model may generate JSON inputs for.",
    )
    function_call: Optional[FunctionCall] = Field(
        None,
        description="Controls how the model calls functions. Valid values are 'none', 'auto', or a specific function name.",
    )
    temperature: Optional[float] = Field(
        None, description="Sampling temperature to use, between 0 and 2."
    )
    top_p: Optional[float] = Field(
        None, description="Nucleus sampling probability, between 0 and 1."
    )
    n: Optional[int] = Field(
        None,
        description="Number of chat completion choices to generate for each input message.",
    )
    stream: Optional[bool] = Field(
        False, description="If set to True, partial message deltas will be sent."
    )
    stop: Optional[Union[str, List[str]]] = Field(
        None, description="Sequences where the API will stop generating further tokens."
    )
    max_tokens: Optional[int] = Field(
        None,
        description="The maximum number of tokens to generate in the chat completion.",
    )
    presence_penalty: Optional[float] = Field(
        0,
        description="Penalizes new tokens based on whether they appear in the text so far.",
    )
    frequency_penalty: Optional[float] = Field(
        0,
        description="Penalizes new tokens based on their existing frequency in the text so far.",
    )
    logit_bias: Optional[dict] = Field(
        None,
        description="Modifies the likelihood of specified tokens appearing in the completion.",
    )
    user: Optional[str] = Field(
        None, description="A unique identifier representing your end-user."
    )

    def create(self):
        return openai.ChatCompletion.create(**self.model_dump(exclude_none=True))

    async def acreate(self):
        return openai.ChatCompletion.acreate(**self.model_dump(exclude_none=True))

    def iterator(self):
        response = self.create()
        message = Message.from_response(response)
        yield message

        self.messages.append(message)

        while message.function_call is not None:
            funcs = list(
                filter(lambda f: f.name == message.function_call.name, self.functions)
            )

            if len(funcs) != 1:
                raise ValueError

            func: Function = funcs[0]
            kwargs = json.loads(message.function_call.arguments)
            print(
                f'Running {func.name}({", ".join([f"{k}={v}" for k, v in kwargs.items()])})'
            )

            if not func.auto_execute:
                a = input("Approve? [y/n]: ")
                if a.lower() != "y":
                    raise KeyboardInterrupt("User denied function execution.")

            result = func.callable(**kwargs)
            print(result)

            self.messages.append(
                Message(
                    role="function",
                    name=func.name,
                    content=json.dumps(result) if type(result) is not str else result,
                )
            )

            response = self.create()
            message = Message.from_response(response)
            yield message

            self.messages.append(message)
