import { initializeApp } from "https://www.gstatic.com/firebasejs/9.22.2/firebase-app.js" ;
import { getFirestore, getDocs, collection, orderBy, limit, query } from 'https://www.gstatic.com/firebasejs/9.22.2/firebase-firestore.js';

const firebaseConfig = {
  apiKey: "AIzaSyBxmKnfbTFFwqJSymyUiSSDimSNWsXaDt8",
  authDomain: "bridge-strike-1d751.firebaseapp.com",
  projectId: "bridge-strike-1d751",
  storageBucket: "bridge-strike-1d751.appspot.com",
  messagingSenderId: "975498392946",
  appId: "1:975498392946:web:7674e8be9bd21788d259eb"
};
    
const app = initializeApp(firebaseConfig);
const db = getFirestore(app);

function loadTwitterWidgets() {
  window.twttr = (function(d, s, id) {
    var js, fjs = d.getElementsByTagName(s)[0],
    t = window.twttr || {};
    if (d.getElementById(id)) return t;
    js = d.createElement(s);
    js.id = id;
    js.src = "https://platform.twitter.com/widgets.js";
    fjs.parentNode.insertBefore(js, fjs);
    
    t._e = [];
    t.ready = function(f) {
      t._e.push(f);
    };
    return t;
  }(document, "script", "twitter-wjs"));
}

function duration(millis) {
  return {
    seconds: Math.floor((millis/1000)%60),
    minutes: Math.floor((millis/(1000*60))%60),
    hours: Math.floor((millis/(1000*60*60))%24),
    days: Math.floor(millis/(1000*60*60*24)),
  };
}

function setTweet(link) {
  document.getElementById("tweet-link").setAttribute("href",`${link}?ref_src=twsrc%5Etfw`);
}
  
function getLatest() {
  getDocs(query(collection(db,"tweets"),orderBy("time","desc"),limit(1))).then(querySnapshot => {
    querySnapshot.forEach((doc) => {
      const tweet = doc.data();
      const time = new Date(tweet.time.seconds*1000);
      setTweet(tweet.link);
      const d = duration(new Date().getTime() - time.getTime())
      document.getElementById("days-val").textContent = d.days;
      loadTwitterWidgets();
    });
  });
}

getLatest();