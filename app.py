from sanic import Sanic, response

app = Sanic(__name__)

in_memory_student_db = [
    {
        "name": "Your Name",
        "grade": "Your Grade",
        "roll": 1,
        "email": "youremail@schooldomain.edu",
        "phone": 9999999999,
        "subjects": ["Mathematics", "Physics", "Computer Science"],
        "friends": [
            "your friend A",
            "your friend B",
            "your friend C",
            "your friend D",
        ],
    }
]


@app.get("/")
async def get_student(request):
    id_ = request.args.get("id")
    if int(id_) in range(len(in_memory_student_db)):
        return response.json(in_memory_student_db[int(id_)])
    return response.json(in_memory_student_db)


@app.post("/")
async def post_student(request):
    student = request.json
    in_memory_student_db.append(student)
    return response.json(student)


@app.put("/<id_:int>")
async def update_student(request, id_):
    student = request.json
    if id_ in range(len(in_memory_student_db)):
        in_memory_student_db[id_] = student
    else:
        return response.json({"error": "No Student with given id"})
    return response.json(student)


@app.delete("/<id_:int>")
async def delete_student(request, id_):
    if id_ in range(len(in_memory_student_db)):
        del in_memory_student_db[id_]
    else:
        return response.json({"error": "No Student with given id"})
    return response.json({"message": "Deleted student successfully"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True, auto_reload=True)
