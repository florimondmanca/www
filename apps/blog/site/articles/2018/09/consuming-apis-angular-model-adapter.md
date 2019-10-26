---
title: "Consuming APIs in Angular: The Model-Adapter Pattern"
description: "A TypeScript-friendly pattern to improve how you integrate Angular apps and REST APIs."
image:
  path: "https://images.unsplash.com/photo-1501580121338-18e859f87400?ixlib=rb-0.3.5&ixid=eyJhcHBfaWQiOjEyMDd9&s=979de881b3346f9ab13eacfd08535cfa&auto=format&fit=crop&w=1350&q=80"
  caption: "An angular shot of smooth white balconies on a building in Almería, Spain. Dmitri Popov, unsplash.com"
date: "2018-09-04"
published: true
tags:
  - webdev
  - angular
  - devtips
---

_Update (Feb. 2019): if you're interested in how to use what is built here in components, I wrote a follow-up article: [Displaying Data In Components](/consuming-apis-in-angular-displaying-data-in-components)._

<br>
<hr>
<br>

In a previous post, I wrote about [best practices in REST API design](https://blog.florimondmanca.com/restful-api-design-13-best-practices-to-make-your-users-happy-ag6). These were mostly applicable on the server side.

Since January 2018, I've also been doing **frontend development** with [**Angular**](https://angular.io), both as a hobby and professionally.

Today, I want to talk about architecture and share with you a **design pattern** that has helped me **structure and standardise** the way I integrate **REST APIs** with **Angular frontend applications**.

TL;DR:

> Write a model class and use an adapter to convert raw JSON data to this internal representation.

**Tip**: you can find the final code for this post on GitHub: [ng-courses](https://github.com/florimondmanca/ng-courses).

Let's dive in!

## The problem

What is it that we're trying to solve, exactly?

Most often these days, frontend apps need to interact a lot with **external backend services** to exchange, persist and retrieve data.

A typical example of this, which we're interested in today, is **retrieving data by requesting a REST API**.

These APIs return data in a given **data format**. This format can **change** over time, and it is most likely not the optimal format to use in our Angular apps built with **TypeScript**.

So, the problem we're trying to solve is:

**How can we integrate an API with an Angular frontend app, while limiting the impact of changes and making full use of the power of TypeScript?**

## The course subscription system

As an example, we'll consider a **course subscription system** in which students can apply to courses and access learning material.

Here's the **user story** for the feature we're trying to build:

"_As a student, I want to view the list of courses so that I can register to new courses._"

To allow this, we have been provided with the following API endpoint:

```text
GET: /courses/
```

Its response data (JSON-formatted) looks something like this:

```json
[
  {
    "id": 1,
    "code": "adv-maths",
    "name": "Advanced Mathematics",
    "created": "2018-08-14T12:09:45"
  },
  {
    "id": 2,
    "code": "cs1",
    "name": "Computer Science I",
    "created": "2018-06-12T18:34:16"
  }
]
```

## Why not just `JSON.parse()`?

The quick-and-dirty solution would be to make HTTP calls, apply `JSON.parse()` on the response body, and use the resulting `Object` in our Angular components and HTML templates. As it turns out, Angular's [HttpClient](https://angular.io/guide/http) can do just this for you, so we wouldn't even have to do much work.

In fact, this is how simple a `CourseService` doing this HTTP request would be:

```typescript
import { Injectable } from "@angular/core";
import { HttpClient } from "@angular/common/http";
import { Observable } from "rxjs";

@Injectable({
  providedIn: "root"
})
export class CourseService {
  constructor(private http: HttpClient) {}

  list(): Observable<any> {
    const url = "http://api.myapp.com/courses/";
    return this.http.get(url);
  }
}
```

There are, however, several issues with this approach:

- **Bug-prone**: There is a wide range of potential bugs that won't be caught early on because we don't make use of TypeScript's static typing.
- **High coupling**: any change to the API's data schema will bubble up through the whole code base, even when it doesn't result in functional changes (e.g. renaming fields).

As a result, while the service itself is easy to maintain and easy to read, it definitely won't be the same for the rest of our code base.

## The need to adapt

So if simply using the JSON object is not sufficient, what better options do we have?

Well, let's think about the two issues above.

First, the code was **bug-prone** because we didn't make use of TypeScript's static typing and OOP features (such as classes and interfaces) to **model the data**. One way to fix this would be to create instances of a specific class (the **model**) so that TypeScript can help us work with it.

Second, we encountered **high coupling** with respect to the API data format. This is because we didn't abstract this data format from the rest of our application components. To solve this issue, one way could be to create an **internal data format** and map to this one when processing the API response.

This is it: we have just conceptualized the **Model-Adapter pattern**. It comprises of two elements:

- The **model class** keeps us within the realm of TypeScript, which has indeed tons of advantages.
- The **adapter** acts as the single interface to ingest the API's data and build instances of the model, which we can use with confidence throughout our app.

I find diagrams always help to grasp concepts, so here's one for you:

![The Model-Adapter pattern, visualised.](https://florimondmanca-personal-website.s3.amazonaws.com/media/markdownx/ac486986-40d0-4dab-9dee-a9b3f569e6a1.png)

## Model-Adapter by example

Now that we've seen what the model-adapter pattern is, how about we implement it in our course system? Let's start with the model.

### The `Course` model

This is going to be a simple TypeScript class, nothing too fancy:

```typescript
// app/core/course.model.ts
export class Course {
  constructor(
    public id: number,
    public code: string,
    public name: string,
    public created: Date
  ) {}
}
```

Note how `created` is a `Date` Javascript object, even though the API endpoint gives it to us as a `string` (ISO-formatted date). You can already see the adapter lurking around at this point.

Now that we have the model, let's start writing a service where the actual HTTP requests will be made. We'll see what we come up with.

### Stubbing out the `CourseService`

Because we're going to make HTTP calls, let's first import the `HttpClientModule` in our `AppModule`:

```diff
  // app/app.module.ts
  import { BrowserModule } from '@angular/platform-browser';
  import { NgModule } from '@angular/core';
+ import { HttpClientModule } from '@angular/common/http';

  import { AppComponent } from './app.component';

  @NgModule({
    declarations: [
      AppComponent
    ],
    imports: [
      BrowserModule,
+     HttpClientModule,
    ],
    providers: [],
    bootstrap: [AppComponent]
  })
  export class AppModule { }
```

We can now create the `CourseService`. As per our design, we'll define a `list()` method supposed to return the list of courses obtained from the `GET: /courses/` endpoint.

```typescript
// app/core/course.service.ts
import { Injectable } from "@angular/core";
import { Course } from "./course.model";
import { Observable, of } from "rxjs";

@Injectable({
  providedIn: "root"
})
export class CourseService {
  list(): Observable<Course[]> {
    // TODO
    return of([]);
  }
}
```

As we already mentioned, a good thing about Angular's `HttpClientModule` is that it has built-in support for JSON responses. Indeed, the `HttpClient` will by default parse the JSON body and build a JavaScript object out of it. So let's try and use that here:

```typescript
// app/core/course.service.ts
import { Injectable } from "@angular/core";
import { HttpClient } from "@angular/common/http";
import { Course } from "./course.model";
import { Observable } from "rxjs";

@Injectable({
  providedIn: "root"
})
export class CourseService {
  private baseUrl = "http://api.myapp.com/courses";

  constructor(private http: HttpClient) {}

  list(): Observable<Course[]> {
    const url = `${this.baseUrl}/`;
    return this.http.get(url);
  }
}
```

At this point, TypeScript's compiler will unfortunately rant out (which is a good point!):

![TypeScript is not happy… Why?](https://florimondmanca-personal-website.s3.amazonaws.com/media/markdownx/436c8b5c-edd5-41c6-b346-77c713f9942e.png)

Of course! We haven't built `Course` instances from the raw data we retrieved. Instead, we're still returning an `Observable<Object>`. We can fix this using [RxJS](https://angular.io/guide/rx-library)'s `map` operator. We'll map the data array to an array of `Course` objects:

```typescript
// app/core/course.service.ts
import { Injectable } from "@angular/core";
import { HttpClient } from "@angular/common/http";
import { Course } from "./course.model";
import { Observable } from "rxjs";
import { map } from "rxjs/operators";

@Injectable({
  providedIn: "root"
})
export class CourseService {
  private baseUrl = "http://api.myapp.com/courses";

  constructor(private http: HttpClient) {}

  list(): Observable<Course[]> {
    const url = `${this.baseUrl}/`;
    return this.http
      .get(url)
      .pipe(
        map((data: any[]) =>
          data.map(
            (item: any) =>
              new Course(item.id, item.code, item.name, new Date(item.created))
          )
        )
      );
  }
}
```

Phew! This will work fine and return an `Observable<Course[]>` as expected.

However, this code has **a couple of issues**:

- It is **hard to read** as the adaptation code clutters the service.
- It is **not DRY** (Don't Repeat Yourself): we'd need to reimplement this logic in all other methods that need to build courses from an API item.
- It puts **high cognitive load** on the developer: we need to refer to the `course.model.ts` file to make sure we provide the correct arguments to `new Course()`.

So, there must be a **better way**…

### Enter: the adapter

And of course, there is! 🎉

This is when the **adapter** comes in. If you're familiar with Gang of Four's design patterns, you might recognize the need for a [Bridge](https://sourcemaking.com/design_patterns/bridge) here:

> Decouple an abstraction from its implementation so that the two can vary independently.

This is exactly what we need (but we'll call it an adapter instead).

The adapter essentially converts the API's representation of an object to our internal representation of it.

In fact, we can even define a generic interface for adapters like so:

```typescript
// app/core/adapter.ts
export interface Adapter<T> {
  adapt(item: any): T;
}
```

So let's build the `CourseAdapter`. Its `adapt()` method will take a single course item (as returned by the API) and build a `Course` model instance out of it. Where should you place this? I would recommend **inside the model file itself**:

```typescript
// app/core/course.model.ts
import { Injectable } from "@angular/core";
import { Adapter } from "./adapter";

export class Course {
  // ...
}

@Injectable({
  providedIn: "root"
})
export class CourseAdapter implements Adapter<Course> {
  adapt(item: any): Course {
    return new Course(item.id, item.code, item.name, new Date(item.created));
  }
}
```

Note that the adapter is an **injectable**. It means we'll be able to use Angular's dependency injection system, as for any other service: add it to the constructor, and use it right away.

### Refactoring the `CourseService`

Now that we've abstracted most of the logic into the `CourseAdapter`, here's how the `CourseService` looks like:

```typescript
import { Injectable } from "@angular/core";
import { HttpClient } from "@angular/common/http";
import { Course, CourseAdapter } from "./course.model";
import { Observable } from "rxjs";
import { map } from "rxjs/operators";

@Injectable({
  providedIn: "root"
})
export class CourseService {
  private baseUrl = "http://api.myapp.com/courses";

  constructor(private http: HttpClient, private adapter: CourseAdapter) {}

  list(): Observable<Course[]> {
    const url = `${this.baseUrl}/`;
    return this.http.get(url).pipe(
      // Adapt each item in the raw data array
      map((data: any[]) => data.map(item => this.adapter.adapt(item)))
    );
  }
}
```

Note that, now:

- The code is more **DRY**: we have abstracted the logic in a separate element (the adapter) which we can reuse at will.
- The `CourseService` is **more readable** as a result.
- **Cognitive load is reduced** because the model and its adaptation logic are kept in the same file.

I also promised to you that the **Model-Adapter pattern** would help **reduce coupling** between the API and our app. Let's see what happens if we encounter a…

### Data format change!

The guys from the API team have made changes to the API's data format. Here's how a `course` item now looks like:

```json
{
  "id": 1,
  "code": "adv-maths",
  "label": "Advanced Mathematics",
  "created": "2018-08-14T12:09:45"
}
```

They changed the name of the `name` field into `label`!

Previously, everywhere our frontend app used the `name` field, we would have had to change it to `label`.

But we're now safe! Since we have an **adapter** whose role is precisely to map between the API representation and our internal representation, we can simply change how the internal `name` is obtained:

```diff
@Injectable({
  providedIn: 'root'
})
export class CourseAdapter implements Adapter<Course> {

  adapt(item: any): Course {
    return new Course(
      item.id,
      item.code,
-     item.name,
+     item.label,
      new Date(item.created),
    );
  }
}
```

**A one-line change!** And the rest of our app can continue to use the `name` field as usual. Brilliant. ✨

## Good principles always apply

I have been using the **Model-Adapter pattern** in most of my Angular projects that involve **REST API interaction**, with great success.

It has helped me **reduce coupling** and make full use of **the power of TypeScript**.

All in all, it really boils down to sticking to good ol' principles of software engineering. The major one here is the **single responsibility principle** — _every code element should do one thing, and do it well_.

I hope this simple architectural tip will help you **improve the way you integrate APIs in Angular apps**. However, if you've been successful yourself with another approach, I'd love to hear about it!
