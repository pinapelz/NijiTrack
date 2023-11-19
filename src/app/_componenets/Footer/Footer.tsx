
import React from 'react';

const Footer = () => {
  return (
    <footer>
      <div className="text-center">
        <p className="text-bold">
            Information
        </p>
        <p className="text-m">
            Information is collected once per hour. Data collection will stop once a liver has graduated.
            <br/>
            This page is in now way affiliated with ANYCOLOR or with any of the channels listed here.
            <br/>
            Date Started: 2023-03-26
        </p>
        <p className="p-4">
            <a className="hover:underline text-bold" href="https://github.com/pinapelz/Nijitrack">Source Code</a><br/>
            We are currently under construction!
        </p>
      </div>
    </footer>
  );
};

export default Footer;
