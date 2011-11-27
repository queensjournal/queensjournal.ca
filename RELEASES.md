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
* [Cut the DB queries from 1500+ on the story_detail to ~75.](https://github.com/tylerball/queensjournal.ca/commit/8b68ad156ca163165c07421392f37560986b0798)
* [disallow blank pub_date in blog entries](https://github.com/tylerball/queensjournal.ca/commit/4026969efffcdeef9eaf712d03f77c09f7938d68)

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
