# KePub Output Sigil Plugin

This output plugin adds kobo spans in all xhtml files, to every sentence. This is to make to the Kobo reader remember how far you've read into a chapter and it also enables annotating and bookmarking.

When you've ran the plugin, it asks where you want to save it.

It's based code from the Calibre [KePub Output Plugin](https://github.com/jgoguen/calibre-kobo-driver), all credit goes to [jgoguen](https://github.com/jgoguen). I modified it to work in Python 3.

Build (zip) the plugin by running `make`.

## Example

### Input
```
<p>But why? Nobody really knew what was outside, if there was anything out there at all. Historical books suggested the world outside was blasted, lifeless and poisonous. That was, at least, the common and logical assumption. But a ghost story somepony told at my first (and only) slumber party had given me horrible nightmares and still lurked in the shadows of my head: a tale of a pony who somehow got the Stable door open and stepped outside… only to find out that there <i>was</i> no outside! Just a great nothingness that whisked the pony away, devouring her soul so that she was nothingness too.</p>
```

### Output
```
<p><span class="koboSpan" id="kobo.52.1">But why? </span><span class="koboSpan" id="kobo.52.2">Nobody really knew what was outside, if there was anything out there at all. </span><span class="koboSpan" id="kobo.52.3">Historical books suggested the world outside was blasted, lifeless and poisonous. </span><span class="koboSpan" id="kobo.52.4">That was, at least, the common and logical assumption. </span><span class="koboSpan" id="kobo.52.5">But a ghost story somepony told at my first (and only) slumber party had given me horrible nightmares and still lurked in the shadows of my head: </span><span class="koboSpan" id="kobo.52.6">a tale of a pony who somehow got the Stable door open and stepped outside… only to find out that there </span><i><span class="koboSpan" id="kobo.52.7">was</span></i><span class="koboSpan" id="kobo.53.1"> no outside! </span><span class="koboSpan" id="kobo.53.2">Just a great nothingness that whisked the pony away, devouring her soul so that she was nothingness too.</span></p>
```
(Snippet from first chapter of [Fallout: Equestria](https://www.fimfiction.net/story/119190/fallout-equestria))
