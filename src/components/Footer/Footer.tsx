import React from "react";
import Link from 'next/link';


const Footer = () => {
	return (
		<footer>
			<div className="text-center mt-4">
			<Link href="/about">
			  <p className="font-bold hover:underline text-blue-600 animate-pulse">About</p>
			</Link>
				<p className="text-m">
					Created by Pinapelz <br/>
					This page is in no way affiliated with Phase Connect or with any of
					the channels listed here
					<br />
					
				</p>
				<p className="p-4">
					<a
						className="hover:underline text-bold text-blue-600"
						href="https://github.com/pinapelz/Nijitrack"
					>
						Source Code
					</a>
					<br />
				</p>
			</div>
		</footer>
	);
};

export default Footer;
