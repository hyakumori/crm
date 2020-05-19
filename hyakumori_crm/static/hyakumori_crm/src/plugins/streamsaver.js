import streamSaver from "streamsaver";

streamSaver.mitm =
  process.env.NODE_ENV === "production" ? "/static/mitm.html" : "/mitm.html";

export default streamSaver;
