# Pancake Kit

Pancake Kit aims to provide a handy user interface to your Python codes. It provides GUI as a lightweight web app powered by Flask. 

<img src="https://raw.githubusercontent.com/chocolate-icecream/pancakekit/main/images/pancakekit_figure_at_glance.png" width="50%"/>

## Quick tasting

Assume that there is a function that calculates the n*th* Fibonacci number. In three steps, you can prepare a GUI that wraps this function.

```python
from pancakekit import Pancake

def fibonacci(n=10):
    return (fibonacci(n-1) + fibonacci(n-2)) if n >= 2 else n

cake = Pancake()	# Step 1: Make a Pancake instance.
cake.add(fibonacci)	# Step 2: Add your function to the pancake.
cake.serve()		# Step 3: Serve the cake.
```

When you open `http://127.0.0.1:8000/` in a web browser, you will find an input box for entering `n` and a button that invokes `fibonacci()`.

## Adding an interface to your exisiting python script in an instant

```shell
pip -m pancakekit __YOUR_SCRIPT_FILE_NAME__
```



For more details: https://github.com/chocolate-icecream/pancakekit

