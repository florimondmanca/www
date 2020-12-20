---
published: true
title: "Consuming APIs in Angular: Displaying Data In Components"
description: "Learn how to fetch a list of items from a REST API and display it in an Angular component."
date: "2019-02-23"
legacy_url: "/consuming-apis-in-angular-displaying-data-in-components"
category: tutorials
tags:
  - angular
  - webdev
image: "/static/img/articles/angular-apis.jpg"
image_caption: "Blue and white plastic toy. @sheldonnunes, unsplash.com"
---

Welcome back! This article is a follow up to a previous article, [Consuming APIs in Angular: The Model-Adapter Pattern](https://blog.florimondmanca.com/consuming-apis-in-angular-the-model-adapter-pattern). If you haven't read it yet — go check it out! This post will be referencing it quite often.

I had a question from a reader about how the `CourseService` could be used in a component, say, to display the list of courses. This is exactly what we'll cover in this beginner-friendly article.

This post should be helpful to anyone wondering **how to retrieve and display data fetched from an external API**. 😊

## Quick refresher

In the original post, we discussed a design pattern that I use to standardise how my Angular apps communicate with REST APIs: the **Model-Adapter pattern**.

Given the `GET /courses` API endpoint, we built a `Course` model, a `CourseAdapter` and a `CourseService` that can help us fetch the list of courses from the API.

Here's what the project structure looks like for now:

```console
src/app
├── app.component.css
├── app.component.html
├── app.component.ts
├── app.module.ts
└── core
    ├── course.model.ts
    └── course.service.ts
```

The goal here is to build a `CourseListComponent` that fetches the list of courses using the `CourseService`, and displays them in the form of a simple unordered list.

## Let's build!

### Generating the `CourseListComponent`

Okay, let's get started. First, we will generate the component using the [Angular CLI](https://cli.angular.io):

```bash
ng generate component CourseList
```

The TypeScript (TS), HTML and CSS files for the component will be generated under `src/app/course-list/`. Here's what the TS file looks like so far:

```typescript
// course-list/course-list.component.ts
import { Component, OnInit } from "@angular/core";

@Component({
  selector: "app-course-list",
  templateUrl: "./course-list.component.html",
  styleUrls: ["./course-list.component.css"]
})
export class CourseListComponent implements OnInit {
  constructor() {}

  ngOnInit() {}
}
```

### Setting up attributes and templates

As a first step, let's add an empty list of courses on the component:

```diff
  // course-list/course-list.component.ts
  import { Component, OnInit } from '@angular/core';

  @Component({
    selector: 'app-course-list',
    templateUrl: './course-list.component.html',
    styleUrls: ['./course-list.component.css']
  })
  export class CourseListComponent implements OnInit {

+   courses: Courses[];

-   constructor() { }
+   constructor() {
+     this.courses = [];
+   }

    ngOnInit() {
    }

}
```

Next, let's set up the template. Nothing fancy here, we're just using an [`*ngFor`](https://angular.io/guide/displaying-data#showing-an-array-property-with-ngfor) to display each course in its own list item, as well as the [`DatePipe`](https://angular.io/api/common/DatePipe) to format the date.

```html
<!-- course-list/course-list.component.html -->
<ul>
  <li *ngFor="let course of courses">
    <p>
      {{ course.name }} • {{ course.code }} • Created {{ course.created | date
      }}
    </p>
  </li>
</ul>
```

While we're at it, let's update the `AppComponent`'s template to display the list of courses:

```html
<!-- app.component.html -->
<h1>Courses</h1>

<app-course-list></app-course-list>
```

Alright! Let's fire up the browser, and we should be greeted with the "Courses" title and… an empty list. Why? Well, we haven't fetched any course yet!

### Implementing the API endpoint

Before we go and plug the `CourseService` in, remember that for now it refers to `https://api.myapp.com/courses` — and that API doesn't exist!

That said, it would be nice to test the `CourseService` against a live server, wouldn't it?

So, let's build a quick backend API for this exact purpose. I'll be using Python and [Starlette] to provide the `GET /courses` endpoint we need to have access to from the browser.

You don't need to know about Python nor understand the code below, but I'm displaying it here for those interested:

```python
# Install: `pip install starlette uvicorn`
import uvicorn
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from starlette.routing import Route

COURSES = [
    {
        "id": 1,
        "code": "adv-maths",
        "name": "Advanced Mathematics",
        "created": "2018-08-14T12:09:45",
    },
    {
        "id": 2,
        "code": "cs1",
        "name": "Computer Science I",
        "created": "2018-06-12T18:34:16",
    },
]


async def courses_list(request):
    return JSONResponse(COURSES)


routes = [
    Route("/courses", courses_list),
]

middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_headers=["*"],
        allow_methods=["*"],
    ),
]

app = Starlette(routes=routes, middleware=middleware)


if __name__ == "__main__":
    uvicorn.run(app)
```

As you can see, the `GET /courses` endpoint will just return a hardcoded list of courses.

We can fire the API up in a terminal using `$ python app.py`, and leave it running.

### Integrating the API with the `CourseService`

As a last integration step, we need to update the URL which the `CourseService` uses to fetch the courses:

```typescript
// core/course.service.ts
// ...

@Injectable({
  providedIn: "root"
})
export class CourseService {
  private apiUrl = "http://localhost:8000/courses";

  // ...
}
```

### Fetching courses with the `CourseService`

We're now ready to plug the `CourseService` into the `CourseListComponent`!

Here are the steps we'll take to do it:

1. **Import** the service.
2. **Inject** it in the component using Angular's [dependency injection](https://www.angular.io/guide/dependency-injection).
3. In the component's `ngOnInit()` method, get the [RxJS] observable to the list of course and **subscribe** to it.
4. **Store** the fetched list of course on the component so that it gets rendered in the template.

Wondering how that translates into code? Take a look below — I added landmarks for each of the steps above:

```typescript
import { Component, OnInit } from "@angular/core";
import { Course } from "../core/course.model";
// (1) Import
import { CourseService } from "../core/course.service";

@Component({
  selector: "app-course-list",
  templateUrl: "./course-list.component.html",
  styleUrls: ["./course-list.component.css"]
})
export class CourseListComponent implements OnInit {
  courses: Course[];

  // (2) Inject
  constructor(private courseService: CourseService) {
    this.courses = [];
  }

  ngOnInit() {
    // (3) Subscribe
    this.courseService.list().subscribe((courses: Course[]) => {
      // (4) Store
      this.courses = courses;
    });
  }
}
```

### Celebrate

There you go! If we open the browser at `http://localhost:8000`, we see the list of courses displayed in sexy Times New Roman.

![Styling is, indeed, out of the scope of this blog post.](/static/img/angular-apis-courses.png)

## Wrapping up

Alright, let's see what we've achieved here:

1. We generated the `CourseListComponent` using [Angular CLI].
2. We set up the component's `courses` attribute and its [template].
3. We used Python and [Starlette] to build the API endpoint to test our component against.
4. We used the `CourseService` and [RxJS] to fetch the list of course.

In fact, this is quite a typical workflow for me when I build web apps using Angular — I start by stubbing out the components, then implement the backend endpoints I need, and integrate them with the services to finally display the data.

If you're interested in the code, I uploaded it to a GitHub repo: [ng-courses](https://github.com/florimondmanca/ng-courses).

[starlette]: https://www.starlette.io
[angular cli]: https://cli.angular.io
[rxjs]: https://angular.io/guide/rx-library
