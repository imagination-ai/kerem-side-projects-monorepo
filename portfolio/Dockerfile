#### 1. Builder
FROM node:latest as build

WORKDIR /app
ENV PATH /app/node_modules/.bin:$PATH

RUN npm ci --silent
RUN npm install react-scripts@3.4.1 -g --silent

COPY portfolio/package.json .
RUN npm install


#### 2. Leaf
#FROM nginx:stable-alpine
#COPY --from=build /app/build /usr/share/nginx/html

COPY portfolio /applications/portfolio

WORKDIR /applications/portfolio

EXPOSE 3000

COPY entrypoints/portfolio-app-entrypoint.sh /applications/portfolio-app-entrypoint.sh
ENTRYPOINT ["sh", "/applications/portfolio-app-entrypoint.sh"]
#EXPOSE 80
#CMD ["nginx", "-g", "daemon off;"]
