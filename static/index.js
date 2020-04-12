function limitChat()
{
  if (document.querySelector("#postim").lenght > 5){
    document.querySelector("#postim").shift();
  }
}
