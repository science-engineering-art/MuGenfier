import { ChangeEvent, MouseEvent, useState } from 'react';

const GenreClassifier = () => {  
  const [music, setMusic] = useState<File>();
  const [genre, setGenre] = useState<string>("");
  const [wasThereClassified, setWasThereClassified] = useState<boolean>(false);

  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    if (e.target.files === null) 
      return;
    setMusic(e.target.files[0]);
    setGenre("");
    setWasThereClassified(false);
  }

  const handleSubmit = async (e: MouseEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (!music) return;

    var form = new FormData();
    form.append("file", music);
  
    await fetch('http://localhost:5000/', {
      method: 'POST',
      body: form
    }).then(res => res.json())
      .then(data => {
        setGenre(data.genre)
        setWasThereClassified(true);
    }).catch(e => console.log(e))
  }

  return (
    <div>
      {wasThereClassified ? <h1>{genre}</h1> : <h1>Select a song:</h1>}
      <form onSubmit={handleSubmit}>
        <input 
          title='File'
          type='file' 
          onChange={handleChange}
          />
        <input type='submit' value={'Classify'}/>
      </form>
    </div>
  );
}

export default GenreClassifier;
