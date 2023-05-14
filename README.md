# Sandbox testing:

### To run:
cd /home/rmslick/PointCloudBrowser/sandbox_testing 

```bash
#start the sandbox server
python manage.py runserver
```
```bash
# open terminal and run
curl --header "Content-Type: application/json"   --request POST   http://localhost:8000/api/sandbox/ --data '{"script":"print()"}'
```

# Sandbox client side:
- MonacoEditorPython.html
- MonacoEditorPythonSyntax.html : Better syntax highlighting