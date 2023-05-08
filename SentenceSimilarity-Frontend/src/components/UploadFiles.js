import React, { PureComponent } from 'react';
import { FilePond } from 'react-filepond';
import 'filepond/dist/filepond.min.css';
const lowEpsilon = 0.51
const standardEpsilon = 0.59
const highEpsilon = 0.67

class UploadFiles extends PureComponent{
    constructor(props) {
      super(props);
      this.state = {
          allFiles: [],
          invalidFiles: [],
          min_samples: 3,
          epsilon: standardEpsilon
      };
    }

    onSubmitFiles = e => {
        e.preventDefault();
        const files = this.state.allFiles;
        var filenames = [];
        for (let i = 0; i < files.length; i++) {
          filenames.push(files[i].filename);
        }

        this.props.onFilesSubmit(filenames, this.state.min_samples, this.state.epsilon);
    }
    
    disableFindSimilaritiesButton= () => {
        const files = this.state.allFiles;
        if (files.length === 0) {
            return true;
        }
        for (let i = 0; i < files.length; i++) {
            console.log(files[i].getStatus);
            if (!files[i].fileType.includes("text")) {
                return true;
            }
        }

        return false;
    }

    onMinSamplesChange = e => {
        const value = e.target.value;
        if (value%1 === 0) {
            this.setState({min_samples: e.target.value});
        }
    }

    render() {
        return (
            <div id="myfilepond">
                <form className="ui form" onSubmit={this.onSubmitFiles}>
                    <div className="field">
                        <label>Upload Files</label>
                        <FilePond ref={ref => this.pond = ref}
                            files={this.state.allFiles}
                            allowMultiple={true}
                            server="http://127.0.0.1:5000/upload"
                            labelIdle={'Drag and Drop your text files or <span class="filepond--label-action"> Browse </span>'}
                            onprocessfile={(error, file) => {
                                if (error && (!file.fileType.includes("text"))) {
                                alert(file.fileType + " is not a valid file type\nOnly text files are accepted")
                                var invalidFiles = this.state.invalidFiles
                                invalidFiles = invalidFiles.push(file)
                                this.setState({invalidFiles})
                                } 
                            }}
                            onremovefile={(error, file) => {
                                if (this.state.invalidFiles.includes(file)) {
                                    const invalidFiles = this.state.invalidFiles.filter(f => f !== file);
                                    this.setState({invalidFiles})
                                }
                            }}
                            onupdatefiles={(fileItems) => {
                                // Set current file objects to this.state
                                this.setState({
                                    allFiles: fileItems,
                                    validFiles: fileItems
                                });
                            }}>
                            </FilePond>
                    </div>
                    <div className="field">
                        <label>Cluster Inclusivity</label>
                        <p>Adjust how similar sentences must be to be included in a cluster together</p>
                        <div id="ClusterInclusivity" className="ui buttons">
                            <button 
                                className={this.state.epsilon === lowEpsilon ? 'ui active button' : 'ui button'} 
                                onClick={e => {
                                    e.preventDefault();
                                    this.setState({epsilon: lowEpsilon});
                                }}>Paraphrase</button>
                            <button 
                                className={this.state.epsilon === standardEpsilon ? 'ui active button' : 'ui button'} 
                                onClick={e => {
                                    e.preventDefault();
                                    this.setState({epsilon: standardEpsilon});
                                }}>Close Sentiment</button>
                            <button 
                                className={this.state.epsilon === highEpsilon ? 'ui active button' : 'ui button'} 
                                onClick={e => {
                                    e.preventDefault();
                                    this.setState({epsilon: highEpsilon});
                                }}>Similar Topic</button>
                        </div>
                    </div>
                    <div className="field">
                        <label>Minimum Cluster Size</label>
                        <input id="MinSamplesInput" type="number" value={this.state.min_samples} onChange={this.onMinSamplesChange} />
                    </div>
                    <button 
                        className="ui big blue button" 
                        disabled={this.disableFindSimilaritiesButton()}
                        type="submit"
                        id="findSimilaritiesButton"
                    >
                        Find Similarities
                    </button>
                </form>
            </div>
        )
    }


}

export default UploadFiles;
