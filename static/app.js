function processVoice() {
  const micButton = document.querySelector(".btn-red");
  micButton.classList.add("listening");

  fetch("/process_voice", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((response) => response.json())
    .then((data) => {
      alert(data.message);
      micButton.classList.remove("listening");
    })
    .catch((error) => {
      console.error("Error:", error);
      alert("There was an error processing your request.");
      micButton.classList.remove("listening");
    });
}
