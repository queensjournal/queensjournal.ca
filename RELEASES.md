Picasso 2.2.4 - August 14, 2012
---------------------------

* fixed pipeline issue
* fixed feeds
* fixed order of latest stories on home page

Picasso 2.2.3 - July 4, 2012
---------------------------

* issue\_detail redesign
* misc cleanup

Picasso 2.2.2 - July 2, 2012
---------------------------

* fixed blog links on front page
* misc fixes

Picasso 2.2.1 - July 1, 2012
---------------------------

* fixed some tests
* fixed some 500s on blogs
* added tests for blog pages


Picasso 2.2 - June 20, 2012
---------------------------

Huge changes. See commits: https://github.com/queensjournal/queensjournal.ca/commits/

* testing
* load\_devdata and dump\_devdata
* reorganization of lots of code
* requirements file simplification

Picasso 2.1.6 - March 10, 2012
------------------------------

Major changes:
* [Moved archive stuff to it's own app](https://github.com/tylerball/queensjournal.ca/commit/9bc6dd1c74f259837eaa048721be710e61d38ad1)

Fixes:
* [removing QuerySetChain for a better combined sort on the front page](https://github.com/tylerball/queensjournal.ca/commit/acbf3ed4b5ad0151d79a220b93b7f8d1b6e8826e)
* [better organization ](https://github.com/tylerball/queensjournal.ca/commit/fd3e14921d760a70360f1a735a9497f97fdd5caa)[of contrib apps](https://github.com/tylerball/queensjournal.ca/commit/8044193a857fb49f4bf3f6657c8d9085884c4b0f)


Picasso 2.1.5.1 - December 14, 2011
-----------------------

Fixes:

* [Fixed an
  importerror](https://github.com/tylerball/queensjournal.ca/commit/6b8715cf8f716fd570d8a337384e2f679c62d8ca)
* [Throw 404 if no Front
  Config](https://github.com/tylerball/queensjournal.ca/commit/5dd0b85d995afd85440e6e1a571dea1fa0e82bb9)
* [moar](https://github.com/tylerball/queensjournal.ca/commit/ac86c208e03c8f7973f04b9ccc6c452025c66b9c)
  [admin](https://github.com/tylerball/queensjournal.ca/commit/4f68e2c1aa3a9c995d769649debfdb946bc5b4ea)
* [turn off thumbnail
  pre-caching](https://github.com/tylerball/queensjournal.ca/commit/340c629a29fe48d3823bcff2a64f6f74e3322e78)
* [fix thumbnail display in search
  results](https://github.com/tylerball/queensjournal.ca/commit/e3c27831dbcf386c7be9abeb17b782f0dbd47026)

Picasso 2.1.5 - November 27, 2011
------------------------

Features:

* [Replaced the date\_diff template filter with a more accurate
  one](https://github.com/tylerball/queensjournal.ca/commit/a00af8de4c02b0cde62190dee5f07a3a2e5a5b0a)
* [Moved tag stuff to own
  app](https://github.com/tylerball/queensjournal.ca/commit/d72033b70d6f024a8c067b4e408d7a8d7674e9e1)
* [Replaced tag encoding with django's urlencode to enable unicode
  tags](https://github.com/tylerball/queensjournal.ca/commit/3a3bff5ec9671ca2177aa8377d400bf5e4f0610e)

Fixes:

* [Fixed some datetime import
  problems](https://github.com/tylerball/queensjournal.ca/commit/4276cf6ddf392500de04373bb833db58afd06365)
* [Removed some unnecessary context
  processors](https://github.com/tylerball/queensjournal.ca/commit/1b16f4ab10f356289b823f38dcdb610976fc5356)

Picasso 2.1.4.1 - November 27, 2011
---------------------

Fixes:

* [Limiting querysets of photos and galleries in the story admin to cut down on database
  queries](https://github.com/tylerball/queensjournal.ca/commit/a8fa1ea0b9e8f1a34167ec5378d884b71a32fc96)
* [Epic cleanup. Fixed indentation, textwidths, removed unused
  files.](https://github.com/tylerball/queensjournal.ca/commit/9b0e780b637c61a6a41d1e7cf06255c32cfdb48f)

Picasso 2.1.4 - November 7, 2011
------------------------------

Features:

* [added robots.txt](https://github.com/tylerball/queensjournal.ca/commit/2a3a8743c66ff6b59e9c5cff5b9bd7a92e54f8df)
* Settings, urls and template cleanup to conform with my best practices:
    * [1](https://github.com/tylerball/queensjournal.ca/commit/72699d41779e1449ab9c281134a95bb8e704f5a4)
    * [2](https://github.com/tylerball/queensjournal.ca/commit/98476e6bf237f481d8139b09d9e4e48af86c1225)
    * [3](https://github.com/tylerball/queensjournal.ca/commit/9b33306f3b9deaa05d6880eb6be4150a5ad4ffa0)
    * [4](https://github.com/tylerball/queensjournal.ca/commit/cbc890bbac9ca273b1645aa27fb2d04b7fea3c1c)
    * [5](https://github.com/tylerball/queensjournal.ca/commit/f5ccf9da76690f8ec95cf5114bceb2c4cab3fbfd)

Fixes:

* [Cut the DB queries from 1500+ on the story\_detail to ~75.](https://github.com/tylerball/queensjournal.ca/commit/8b68ad156ca163165c07421392f37560986b0798)
* [disallow blank pub\_date in blog entries](https://github.com/tylerball/queensjournal.ca/commit/4026969efffcdeef9eaf712d03f77c09f7938d68)

Picasso 2.1.3 - October 10, 2011
--------------------------------

Features:

* [Added verification file for Google webmaster tools](https://github.com/tylerball/queensjournal.ca/commit/6e48c4947928a8ae79c058fc12cd7f91769ad4a6)
* [Filter unpublished items from author pages](https://github.com/tylerball/queensjournal.ca/commit/0761f1a1062d456764e362771b1d018dc960f776)

Fixes:

* [Fixed error when story added to issue with no FrontConfig](https://github.com/tylerball/queensjournal.ca/commit/b7f1085307f5bc2b824862f784bcc3fac3fb502e)
* [Removed PhotosPageOptions, will find a better solution](https://github.com/tylerball/queensjournal.ca/commit/e4135aa1aecf410d3817d352a3c241a2a3e38e90)
* Added submodules for [some](https://github.com/tylerball/queensjournal.ca/commit/e4135aa1aecf410d3817d352a3c241a2a3e38e90) [dependencies](https://github.com/tylerball/queensjournal.ca/commit/4077cfafe65534986c9340453f3887cbf3123841), in order to pass tests.

Picasso 2.1.2 - September 13, 2011
----------------------------------

Fixes:

* Removed 'Canada's Oldest Student Newspaper'

Picasso 2.1.1 - September 12, 2011
----------------------------------

Features:

* Implemented mobile site.
* Fabric pulldump command for pulling postgres dumps and loading them locally
* Image admin for embedded blog images

Fixes:

* b2f3387, f8bf9dd - Fixed photorequest instance user has no author.
* cddb1e3 - cleanup
* 2e5be28 - proper server email settings

Picasso 2.1 - August 28, 2011
-----------------------------

Fixed Photo Requests.

***

Picasso 2.0 - March 20, 2011
----------------------------
