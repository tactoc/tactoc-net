import React, { ChangeEvent } from "react";
import * as tus from "tus-js-client";
import "./App.css";

interface IState {
  file: File | null;
  uploadedBytes: Number;
  totalBytes: Number;
  status: string;
  uploadUrl: string | null;
}

export default class App extends React.Component<any, IState> {
  constructor(props: any) {
    super(props);
    this.state = {
      uploadedBytes: 0,
      totalBytes: 0,
      status: "No file selected",
      uploadUrl: "",
      file: null,
    };
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  getFileExtension(uri: any) {
    const match = /\.([a-zA-Z]+)$/.exec(uri);
    if (match !== null) {
      return match[1];
    }

    return "";
  }

  getMimeType(extension: any) {
    if (extension === "jpg") return "image/jpeg";
    return `image/${extension}`;
  }

  handleSubmit(event: any) {
    event.preventDefault();
    const extension = this.getFileExtension(this.state.file?.name)
    const upload = new tus.Upload(this.state.file as File, {
      endpoint: "http://localhost:8088/files",
      retryDelays: [0, 1000, 3000, 5000],
      metadata: {
        filename: `photo.${extension}`,
        filetype: this.getMimeType(extension),
      },
      onError: (error) => {
        this.setState({
          status: `upload failed ${error}`,
        });
      },
      onProgress: (uploadedBytes, totalBytes) => {
        this.setState({
          totalBytes,
          uploadedBytes,
        });
      },
      onSuccess: () => {
        this.setState({
          status: "upload finished",
          uploadUrl: upload.url,
        });
        console.log("Upload URL:", upload.url);
      },
    });

    upload.start();

    this.setState({
      status: "upload started",
      uploadedBytes: 0,
      totalBytes: 0,
      uploadUrl: null,
    });
  }

  handleFileChange = (event: ChangeEvent<HTMLInputElement>) => {
    if (event.target.files) {
      this.setState({
        file: event.target.files[0],
      });
    }
  };

  render() {
    return (
      <div className="App">
        <h1>Hello</h1>
        <form onSubmit={this.handleSubmit}>
          <label>
            Upload file:
            <input type="file" onChange={this.handleFileChange} />
          </label>
          <br />
          <button type="submit">Upload</button>
        </form>
      </div>
    );
  }
}
