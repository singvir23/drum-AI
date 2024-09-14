import React, { useRef} from 'react';
import { OpenSheetMusicDisplay } from 'opensheetmusicdisplay';

const MusicSheet = () => {
  const osmdRef = useRef(null);
  const fileInputRef = useRef(null);

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        const osmd = new OpenSheetMusicDisplay(osmdRef.current, {
          autoResize: true,
          drawTitle: true,
        });
        osmd.load(e.target.result)
            .then(() => osmd.render())
            .catch(error => console.error("Error loading the MusicXML file: ", error));
      };
      reader.readAsText(file);
    }
  };

  return (
    <div>
      <input ref={fileInputRef} type="file" onChange={handleFileChange} accept=".xml" style={{ margin: '20px' }} />
      <div ref={osmdRef} style={{ width: '100%', height: 'auto', backgroundColor: '#f5f5dc' }}></div>
    </div>
  );
};

export default MusicSheet;
