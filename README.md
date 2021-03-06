<div align="center">
    <img width="128" src="./brand/logo.png" alt="OcellusScript logo">
    <h1>OcellusScript</h1>
</div>

[![MPL](https://img.shields.io/github/license/alicerunsonfedora/ocellusscript)](LICENSE.txt)
 ![Java CI with Gradle](https://github.com/alicerunsonfedora/ocellusscript/workflows/Java%20CI%20with%20Gradle/badge.svg?branch=master)

OcellusScript is a simple multi-paradigm programming language modeled after Java and Haskell while combining features from other languages like Kotlin, Swift, Python, and JavaScript. Although designed specifically for the [Unscripted](https://unscripted.marquiskurt.net) visual novel, this language can be used separately with JVM and WebAssembly.

> ⚠️ This project has been deprecated in favor of [Fira](https://github.com/alicerunsonfedora/fira), the minigame engine for Unscripted with API support.

## Quick Links

- [Compiler](./compiler/)
- [Visual Studio Code Extension](./vslang/)

## Repository Contents

This project repository contains the following subprojects:

- The NOC compiler for OcellusScript, implemented in Kotlin
- The Visual Studio Code extension with language syntax support
- The TextMate language bundle with language syntax support
- The brand logos and color palette

## Example Code

```ocls
# Either use OcellusScript functionally...
func mult takes Integer and Integer returns Integer;
```Multiply two numbers together.```
func mult = (x, y) => (x * y);

# Or use it the object-oriented style!
class Example = {
    private var test = "world";

    func init takes String returns Example;
    func init = (t) => {
        self.test = t;
        return self;
    };

    func hello takes Example returns String;
    func hello = (self) => "Hello, " + self.test + "!";
}
```

## Submit a proposal

If you wish to make a proposal to add a feature to OcellusScript, feel free to write one on YouTrack. [Submit a proposal &rsaquo;](https://youtrack.marquiskurt.net/youtrack/newIssue?project=OCLS)
