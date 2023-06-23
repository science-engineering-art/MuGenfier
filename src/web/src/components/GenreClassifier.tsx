import { ChangeEvent, MouseEvent, useState } from 'react';
import Dropdown, { Option } from 'react-dropdown';


const options: Option[] = [
  { value: 'cnn_mfcc', label: 'CNN + MFCC' },
  { value: 'dwt', label: 'Random Forest + Wavelet' },
  { value: 'vision_lang', label: 'Vision Language Model' },
];


const GenreClassifier = () => {  
  const [music, setMusic] = useState<File>();
  const [genre, setGenre] = useState<string>("");
  const [wasThereClassified, setWasThereClassified] = useState<boolean>(false);
  const [selectedOption, setSelectedOption] = useState(options[0]);


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

    const model = selectedOption['value']

    console.log(model)
  
    await fetch(`http://localhost:8000/${model}`, {
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
      <Dropdown 
        options={options} 
        onChange={(op: Option) => setSelectedOption(op)} 
        value={selectedOption} 
      />
    </div>
  );
}

export default GenreClassifier;
