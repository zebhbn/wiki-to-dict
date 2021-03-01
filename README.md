# wiki-to-dict
Generate a kindle dictionary from a MediaWiki website
Works with varying degree of success, depending on how well the wiki pages are scructered
Change the URL fields in generator.py to the api.php url and run generator.py to generate the content.html file.
Use the other html and opf files as templates and then finally run ./kindlegen dict.opf -c2 -o dictionary.mobi
