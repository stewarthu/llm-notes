import json
from typing import Optional
from pydantic import BaseModel, Field
from enum import Enum

class APICallParameters(BaseModel):
    api_name: str = Field(
        ...,
        description="APIs to call: 1. Movement API: it returns the weekly movement, sales, and margin data; 2. Price API: it returns the weekly regular prices; 3. Cost API: it returns the weekly list costs for all items; 4. Promotion API: it returns the weekly promotion types and sale prices.",
        enum=["movement", "price", "cost", "promotion"]
    )
    product_name: str = Field(
        ...,
        description="Used to specify which product group the user wants data pertaining to. For example, 'Upper Respiratory' or 'grocery' would be valid ways of using this argument."
    )
    item_list: Optional[str] = Field(
        None,
        description="A list of items the user wants data pertaining to."
    )
    location_name: str = Field(
        ...,
        description="Used to specify the location the user wants data pertaining to. For example, 'Zone 620' or 'online stores' would be valid ways of using this argument."
    )
    week: Optional[str] = Field(
        None,
        description="Can be used to specify specific weeks in the retail calendar, e.g., 'week' = 7 or 'week' = [46, 47, 48]. Alternatively, the user can specify certain weeks using key phrases such as 'current', 'last 4', or 'next 6'."
    )
    period: Optional[str] = Field(
        None,
        description="Can be used in a similar way as 'week', only return the numerical value"
    )
    quarter: Optional[str] = Field(
        None,
        description="Can be used in a similar way as 'week', only return the numerical value"
    )
    cal_year: Optional[str] = Field(
        None,
        alias="cal-year",
        description="Can be used in a similar way as 'week', only return the numerical value"
    )
    start_date: Optional[str] = Field(
        None,
        alias="start-date",
        description="Can be used to specify that the user wants information from a certain date onwards, e.g., 'May 12, 2021'."
    )
    end_date: Optional[str] = Field(
        None,
        alias="end-date",
        description="Same as start-date"
    )
    promoted: Optional[str] = Field(
        None,
        description="A flag that only applies to Movement API: the API will pull promoted data if this flag is set to true.",
        enum=["True", "False"]
    )

class PostProcessParameters(BaseModel):
    data_file: str = Field(
        ...,
        description="Data file to be loaded to get the Pandas Data Frame."
    )
    action: str = Field(
        ...,
        description="A function to be applied to the Data Frame",
        enum=["mean", "sum", "detect-change"]
    )
    cols: str = Field(
        ...,
        description="Column or list of columns selected for post processing"
    )

if __name__ == '__main__':
    print(APICallParameters.schema())
    print(PostProcessParameters.schema())
    function_signatures = [APICallParameters.schema(), PostProcessParameters.schema()]

    file_name = 'func-signatures2.json'
    with open(file_name, 'w') as file:
        json.dump(function_signatures, file)

    with open(file_name, 'r') as file:
        data = json.load(file)
    print(data)
