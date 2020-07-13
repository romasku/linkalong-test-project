FROM node:14.5-alpine as builder

RUN mkdir /app

WORKDIR /app

COPY package.json package-lock.json ./

RUN npm install

COPY src ./src
COPY babel.config.js tsconfig.json .eslintrc.js .browserslistrc ./

RUN npm run build

FROM nginx:1.15.7-alpine

COPY docker/nginx/default.conf /etc/nginx/conf.d/

RUN rm -rf /usr/share/nginx/html/*

RUN mkdir /linlalong-frontend

WORKDIR /linlalong-frontend

COPY --from=builder /app/dist /usr/share/nginx/html
COPY docker/startup.sh ./

CMD ./startup.sh
