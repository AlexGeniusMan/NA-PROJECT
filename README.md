# NA-PROJECT
📰 "News-Agency" is an open-source project, that works like news portal.

Users can view:
1. Recent news
2. Most pupular news
3. Pinned news
4. News of selected categories
5. Coronavirus statistics
6. Сurrency statistics

Admins can:
1. Add news
2. Pin news
3. Change news
4. Delete news

## Launching project in production mode
#### Git, Docker and Docker Compose must be installed

1. Clone project with submodules

```
git clone https://github.com/AlexGeniusMan/NA-PROJECT news
cd news
git submodule init
git submodule update
```

2. Generate new DJANGO_SECRET_KEY and paste it to news_backend service as SECRET_KEY environment variable in docker-compose.yml

> To generate new DJANGO_SECRET_KEY use this instruction: https://stackoverflow.com/a/57678930/14355198

```
services:
  news_backend:
    environment:
      - SECRET_KEY=NEW_DJANGO_SECRET_KEY
```

3. Put your PRODUCTION_URL to news_frontend service as YOUR_PRODUCTION_URL environment variable in docker-compose.yml
```
services:
  news_frontend:
    environment:
      - REACT_APP_PRODUCTION_URL=http://YOUR_PRODUCTION_URL:8000/
```

4. Launch project

```
docker-compose up --build
```

> Done! Project launched on 8000 port!

<!---

-->

This project was made by RealityGang - team of RTU IT Lab.
