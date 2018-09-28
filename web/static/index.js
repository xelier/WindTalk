function FormattedDate(props) {
  return <h2>现在是 {props.date.toLocaleTimeString()}.</h2>;
}
 
class Clock extends React.Component {
  constructor(props) {
    super(props);
    this.state = {date: new Date()};
  }
  componentDidMount() {
    this.timerID = setInterval(
      () => this.tick(),
      1000
    );
  }
 
  componentWillUnmount() {
    clearInterval(this.timerID);
  }
 
  tick() {
    this.setState({
      date: new Date()
    });
  }
 
  render() {
    return (
      <div>
        <h1>Hello, world!</h1>
        <FormattedDate date={this.state.date} />
      </div>
    );
  }
}
 
ReactDOM.render(
  <Clock />,
  document.getElementById('example')
);



class UserGist extends React.Component {
  constructor(props) {
      super(props);
      this.state = {username: '', lastGistUrl: ''};
  }

  cancleToken() {
    let CancelToken = axios.CancelToken;
    return CancelToken.source();
  }
  getHost(){
      return window.location.host;
  }

  componentDidMount() {
    axios.post(this.props.source,{cancelToken: this.cancleToken().token}).then( function (result) {
      let lastGist = result.data.data[0];
      debugger;
      this.setState({
        username: lastGist.username,
        lastGistUrl: lastGist.profile
      });
    }.bind(this));
  }

  componentWillUnmount() {
      this.cancleToken().cancel();
    // this.serverRequest.abort();
  }

  render() {
    return (
      <div>
        {this.state.username} 用户最新的 Gist 共享地址：
        <a href={this.state.lastGistUrl}>{this.state.lastGistUrl}</a>
      </div>
    );
  }
}
ReactDOM.render(
  <UserGist source="http://localhost:8888/" />,
  document.getElementById('userInfo')
);
