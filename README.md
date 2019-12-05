# Just another Data Offline Generator - JDOG :dog:
- JDOG is Python library which helps generate sample data for your projects. 
- JDOG can be run also as CLI tool.
- For generating sample data, the data scheme is provided
- Scheme is in JSON like format

## Scheme
- Scheme of data is provided as file in JSON format with special placeholders. 
- Placeholder is, special place within JSON, and its purpose is like variable,where generated data will be replaced.
- Output file is nearly the same as scheme besides replaced placeholders.
- In simplest form, given JSON file
```json
{
    "name": "Bob",
    "age" : "18"
}
```
is **valid scheme** although no additional generation will be proceeded. 

```json
{
    "name": "Bob",
    "age": "{{number(18,100)}"
}
```
Now produced data can be Bob with any age between <18, 99> where type is *number*

Let's go wild
```json
[
    "{{range(4)}}": {
        "name": "{{first_name}}",
        "age" : "{{number(18, 100)}}"

    },
]

```
Following schema will generate array with generated objects (name, age). For exmaple: 
```json
[
    {
        "name": "Bob",
        "age" : "18"
    },
    {
      "name": "Alice",
      "age": 25
    },
    {
        "name": "George",
        "age": 85
    },
    {
        "name": "Janice",
        "age": 34
    }
]
```

### Schema placeholders
- *first_name* - generic first name
- *last_name* - generic last name
- *number(l,h)* - number between *l (inlusive)* to *h (exclusive)*
- *age* - number between 1-99 (inclusive)
- *city* - generic city
- *street_address*
- *lorem(n)* - lorem ipsum length of *n-words*
- *option([arg1,...,argn])* - pick randomly on of arg1,..., argn

#### range(l, [h])
Range is like for-each cycle. 

If only *l* provided - generation runs exactly l times
If *h* is proivded - generation runs randomly betwwen *l* (incluive) and *h* (exclusive) times. 

Second option comes handy when you want to have more randomized data. 

## CLI Usage
- [PATH] (Positional argument) Path to scheme
- *-f*, *--format* [FORMAT] Output is in given format {json, xml}. 
- *-s*, *--save* [PATH] Saves output at given path. **Optional**
 
By default, CLI tool does not save output to file, just print results to standard output.  
