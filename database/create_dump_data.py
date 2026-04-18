from database.schema import Unit, Course, UserCourse, User, Material, Lesson, session


users = [
    User(name='AHMAD',    email="ahmad12@gmail.com",    role="admin"),
    User(name='Abdullah', email="abdullah32@gmail.com", role="student"),
    User(name='Ali',      email="ali345@gmail.com",     role="admin"),
    User(name='Sara',     email="sara65@gmail.com",     role="student"),
]
session.add_all(users)
session.flush()

python_course = Course(name="Introduction to Python")
webdev_course = Course(name="Web Development Fundamentals")
data_course   = Course(name="Data Science Basics")
session.add_all([python_course, webdev_course, data_course])
session.flush()

enrolments = [
    UserCourse(user_id=users[0].id, course_id=python_course.id),
    UserCourse(user_id=users[0].id, course_id=webdev_course.id),
    UserCourse(user_id=users[1].id, course_id=python_course.id),
    UserCourse(user_id=users[1].id, course_id=data_course.id),
    UserCourse(user_id=users[2].id, course_id=webdev_course.id),
]
session.add_all(enrolments)

u1 = Unit(title="Getting Started with Python",  course=python_course)
u2 = Unit(title="Control Flow & Functions",      course=python_course)
u3 = Unit(title="HTML & CSS Basics",             course=webdev_course)
u4 = Unit(title="JavaScript Essentials",         course=webdev_course)
u5 = Unit(title="Introduction to Data Analysis", course=data_course)
session.add_all([u1, u2, u3, u4, u5])
session.flush()


l1  = Lesson(title="Setting Up Your Environment", unit=u1)
l2  = Lesson(title="Variables & Data Types",       unit=u1)
l3  = Lesson(title="Control Flow",                 unit=u2)
l4  = Lesson(title="Functions",                    unit=u2)
l5  = Lesson(title="HTML Basics",                  unit=u3)
l6  = Lesson(title="CSS Styling",                  unit=u3)
l7  = Lesson(title="JavaScript Syntax",            unit=u4)
l8  = Lesson(title="JS DOM Manipulation",          unit=u4)
l9  = Lesson(title="Intro to Pandas",              unit=u5)
l10 = Lesson(title="Data Visualization",           unit=u5)
session.add_all([l1, l2, l3, l4, l5, l6, l7, l8, l9, l10])
session.flush()


all_materials = [
    Material(type="video",    file_url="https://cdn.example.com/videos/py-setup.mp4",          lesson=l1),
    Material(type="pdf",      file_url="https://cdn.example.com/docs/py-setup-guide.pdf",       lesson=l1),
    Material(type="video",    file_url="https://cdn.example.com/videos/variables.mp4",          lesson=l2),
    Material(type="quiz",     file_url="https://cdn.example.com/quizzes/variables-quiz",         lesson=l2),
    Material(type="video",    file_url="https://cdn.example.com/videos/control-flow.mp4",       lesson=l3),
    Material(type="pdf",      file_url="https://cdn.example.com/docs/functions.pdf",            lesson=l4),
    Material(type="video",    file_url="https://cdn.example.com/videos/html-basics.mp4",        lesson=l5),
    Material(type="pdf",      file_url="https://cdn.example.com/docs/html-cheatsheet.pdf",      lesson=l5),
    Material(type="video",    file_url="https://cdn.example.com/videos/css-styling.mp4",        lesson=l6),
    Material(type="video",    file_url="https://cdn.example.com/videos/js-syntax.mp4",          lesson=l7),
    Material(type="quiz",     file_url="https://cdn.example.com/quizzes/js-quiz",               lesson=l8),
    Material(type="video",    file_url="https://cdn.example.com/videos/pandas.mp4",             lesson=l9),
    Material(type="notebook", file_url="https://cdn.example.com/notebooks/pandas-intro.ipynb",  lesson=l9),
    Material(type="video",    file_url="https://cdn.example.com/videos/dataviz.mp4",            lesson=l10),
]
session.add_all(all_materials)

session.commit()
print("Database seeded successfully.")