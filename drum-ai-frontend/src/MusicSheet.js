import React, { useState, useRef } from 'react';
import { OpenSheetMusicDisplay } from 'opensheetmusicdisplay';

const MusicSheet = () => {
  const [prompt, setPrompt] = useState("");
  const [loading, setLoading] = useState(false);
  const osmdRef = useRef(null);

  const handleGenerateMusic = async () => {
    setLoading(true);
    try {
      const response = await fetch("http://localhost:3001/generate-xml", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt }),
      });
      const data = await response.json();
      if (data.xml) {
        const osmd = new OpenSheetMusicDisplay(osmdRef.current, {
          autoResize: true,
          drawTitle: true,
        });
        await osmd.load(data.xml);
        osmd.render();
      }
    } catch (error) {
      console.error("Error fetching the MusicXML: ", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <input 
        type="text" 
        value={prompt} 
        onChange={(e) => setPrompt(e.target.value)} 
        placeholder="Enter a music prompt..." 
        style={{ margin: '20px', width: '60%' }}
      />
      <button onClick={handleGenerateMusic} disabled={loading} style={{ margin: '10px' }}>
        {loading ? "Generating..." : "Generate Music"}
      </button>
      <div ref={osmdRef} style={{ width: '100%', height: 'auto', backgroundColor: '#f5f5dc' }}></div>
    </div>
  );
};

export default MusicSheet;
