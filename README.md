# syllashare-django

Install:
```
git clone https://github.com/Tryst480/syllashare-react.git
cd syllashare-react
npm install
npm run build
cd ..
git clone https://github.com/Tryst480/syllashare-django.git
cd syllashare-django
cd syllashare
pip3 install -r requirements.txt
cp -r ../../syllashare-react/build .
sudo python3 manage.py collectstatic
sudo python3 manage.py runserver 0.0.0.0:80
```
