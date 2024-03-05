# frontend/Dockerfile
FROM node

COPY . /workspace
WORKDIR /workspace
RUN npm install && npm install axios

CMD ["npm", "start"]
