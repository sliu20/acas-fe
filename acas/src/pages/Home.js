import React from 'react';

import { exec, execSync } from 'child_process';

function Home() {
    const getDirectory = async () => {
        // const cmd = 'ls';
        // let result = await new Promise(function (resolve, reject) {
        //     exec(cmd, (err, stdout, stderr) => {
        //       if (err) {
        //         reject(err);
        //       } else {
        //         resolve({ stdout, stderr });
        //       }
        //     });
        //   });
        let result;
        try {
            result = execSync('echo "hello world"', { encoding: 'utf-8' });
        }
        catch (error) {
            console.log(error);
        }
       
        console.log(result);
    }
    
    return (
      <p onClick={getDirectory}>Home</p>
    );
}

export default Home;
