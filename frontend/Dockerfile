# frontend/Dockerfile
FROM node:lts-slim

COPY . /workspace
WORKDIR /workspace
RUN npm cache clean --force \
    && rm -rf node_modules package-lock.json \
    && npm install --legacy-peer-deps \
    && npm i -g react-scripts \
    && npm i react-ts-tradingview-widgets \
    && npm install axios

CMD ["npm", "start"]
