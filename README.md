# Django REST Framework Versioning

This project aims to make it easy to support many different API versions in a Django REST Framework (DRF) project.

DRF [supports several versioning schemes](https://www.django-rest-framework.org/api-guide/versioning/) but (perhaps wisely) sidesteps the issue of how to actually deal with the different versions in your code. To quote the docs: "How you vary the API behavior is up to you".

This project provides some out-of-the box tools to handle versioning in views and serializers. The aim is to abstract away any versioning logic into a sort of "versioning layer" and allow the bulk of the code (and its developers) to focus on the latest behaviour.

## Documentation

Please see the full documentation [here](https://binnev.github.io/djangorestframework_versioning/).

## Acknowledgements

The approach taken in this project was inspired by Stripe's API version "compatibility layer", as described in blog posts by [Brandur Leach](https://stripe.com/blog/api-versioning) and [Amber Feng](https://amberonrails.com/move-fast-dont-break-your-api). I used [Ryan Kaneshiro's](https://rescale.com/blog/api-versioning-with-the-django-rest-framework/) excellent Django sketch as a starting point.

I also want to thank my colleagues at [Tranzer](https://www.tranzer.com) for encouraging me to work on this, and for being my guinea pigs / code duckies ❤️