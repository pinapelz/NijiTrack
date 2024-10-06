import React from "react";

const Footer = () => {
	return (
		<footer>
			<div className="text-center mt-4">
			<a className="font-bold hover:underline text-blue-600 animate-pulse"href="/about">About</a>
				<p className="text-m">
					This page is in no way affiliated with Phase Connect or with any of
					the channels listed here.
					<br />
					
				</p>
				<p className="p-4">
					<a
						className="hover:underline text-bold"
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
