# I want to see my archive's files.

usage: `iwts.py a.zip.tar.gz.xz.wahtever` and then u get a folder in your working directory

---

have you ever unzipped a zip file and the contents splattered all over your directory like ketchup?

have you ever extracted a tar archive and the permissions were so messed up
you had to use `sudo rm -rf` or `chmod -R` to remove it even though you made sure to use
`--no-same-owner` and `--no-same-permissions`?

this is the program for you!!!!!

name inspired by https://moonbase.lgbt/blog/i-want-to-see-my-friends-posts/ which isn't really relevent
in the context this was made
but im just tired of things like (insert library) being absolutely esoteric
and (insert wrapper for library) having documentation which is literally full of lies
and is otherwise unhelpful
and (insert command line tool) having enough options that it takes more than 20 minutes to go through
in a domain with so much potential vocabulary that you need a thesaurus if you're gonna search for a feature.

This program is entirely a convenience wrapper over archive extraction.

Simple.  Pona.

* if the entries in the archive aren't all in one folder, it will put them all in one folder.
* regarding permissions and ownership in tar archives,
    * directory permissions will be set to 755
    * file read permissions will be enabled
    * file user-write permissions will be enabled
    * file execute permissions will be preserved
    * owner will not be preserved

usage: `iwts.py a.zip.tar.gz.xz.wahtever`

depends on `unzip` and `tar` and hopefully more things eventually

there are no command line options at this time.  future options may include:
* destination directory
* maybe listing contents of archive?
