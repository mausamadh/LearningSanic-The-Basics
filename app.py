from typing import List
from sanic import Sanic, response
from pydantic import BaseModel, validator
import json

app = Sanic(__name__)
app.config.FALLBACK_ERROR_FORMAT = "json"
a = {
    "name": "your Name",
    "grade": "Your Grade",
    "roll": "2",
    "email": "youremail@schooldomain.edu",
    "phone": "9812345678",
    "subjects": ["Mathematics", "Physics", "Computer Science"],
    "friends": [
        "your friend A",
        "your friend B",
        "your friend C",
        "your friend D",
    ],
}

in_memory_student_db = [a]


class Student(BaseModel):
    name: str
    grade: str
    roll: int
    email: str
    phone: int
    subjects: List[str]
    friends: List[str]

    @validator("name")
    def name_must_contain_space(cls, name):
        if " " not in name:
            raise ValueError("must contain a space")
        return name.title()

    @validator("phone")
    def phone_number_len(cls, phone):
        if len(str(phone)) != 10:
            raise ValueError("Phone number must contain 10 digits")
        return phone

    # use builtin .dict .... there are other .json() and .schema_json() too try that own
    # def serialize(self):
    #     return json.loads(json.dumps(self, default=lambda o: o.__dict__, indent=4))

    # def toJSON(self):
    #     return json.loads(
    #         json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
    #     )


# student = Student(
#     name=in_memory_student_db[0]["name"],
#     grade=in_memory_student_db[0]["grade"],
#     roll=in_memory_student_db[0]["roll"],
#     email=in_memory_student_db[0]["email"],
#     phone=in_memory_student_db[0]["phone"],
#     subjects=in_memory_student_db[0]["subjects"],
#     friends=in_memory_student_db[0]["friends"],
# )
# print("------STUDENT------", student)
# print("------TYPE ---- STUDENT------", type(student))


@app.get("/")
async def get_student(request):
    id_ = int(request.args.get("id", -1))
    print(type(id_), id_)
    if id_ != -1:
        if id_ in range(len(in_memory_student_db)):
            return response.json(in_memory_student_db[id_])
        else:
            return response.json(
                {
                    "status": "error",
                    "message": f"data with id {id_} not found. Try with different id!!!",
                }
            )
    return response.json(in_memory_student_db)


@app.post("/")
async def post_student(request):
    student = Student(**request.json)
    in_memory_student_db.append(student.dict())
    return response.json(student.dict())


@app.put("/<id_:int>")
async def update_student(request, id_):
    student = Student(**request.json)
    if id_ in range(len(in_memory_student_db)):
        in_memory_student_db[id_] = student.dict()
        return response.json(student.dict())
    return response.json({"error": "No Student with given id"})
    


@app.delete("/<id_:int>")
async def delete_student(request, id_):
    if id_ in range(len(in_memory_student_db)):
        del in_memory_student_db[id_]
        return response.json({"message": "Deleted student successfully"})
    return response.json({"error": "No Student with given id"})
    


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True, auto_reload=True)
