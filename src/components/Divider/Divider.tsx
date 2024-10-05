interface DividerProps {
	text: string;
}

const Divider = (props: DividerProps) => {
	return (
		<div className="flex flex-row items-center justify-center bg-black h-24 max-w-full px-72">
			<div className="px-2 text-white text-4xl font-extrabold">
				{props.text}
			</div>
		</div>
	);
};
export default Divider;
