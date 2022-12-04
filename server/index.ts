import tus from "tus-node-server";

const server = new tus.Server({ path: "/files" });
server.datastore = new tus.FileStore({ directory: "./files" });

import express, { Express, Request, Response } from "express";
import dotenv from "dotenv";
var cors = require("cors");

dotenv.config();

const app: Express = express();
const uploadApp: Express = express();
app.use(cors());

uploadApp.all("*", server.handle.bind(server));
app.use("/files", uploadApp);

const port = process.env.PORT;

app.get("/", (req: Request, res: Response) => {
  res.send("Express + TypeScript Server");
});

app.listen(port, () => {
  console.log(`[Server] is running at port ${port}`);
});
