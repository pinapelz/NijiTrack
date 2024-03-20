
import React from 'react';

const Footer = () => {
  return (
    <footer>
      <div className="text-center mt-4">
        <p className="font-bold">
            Information
        </p>
        <p className="text-m">
            Information is collected once per hour. Data collection will stop upon graduation
            <br/>
            This page is in no way affiliated with Phase Connect or with any of the channels listed here.
            <br/>
            Data Collection Started: 2022-04-01 (Earlier data may not be fully accurate)
        </p>
        <p className="p-4">
            <a className="hover:underline text-bold" href="https://github.com/pinapelz/Nijitrack">Source Code</a><br/>
        </p>
      </div>
    </footer>
  );
};

export default Footer;
