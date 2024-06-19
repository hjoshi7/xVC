
        const tryRequire = (path) => {
        	try {
        	const image = require(`${path}`);
        	return image
        	} catch (err) {
        	return false
        	}
        };

        export default {
        
	questionMark: require('./questionMark.png'),
	Frame1_Shapewithtext: tryRequire('./Frame1_Shapewithtext.png') || require('./questionMark.png'),
	Frame7_Shapewithtext: tryRequire('./Frame7_Shapewithtext.png') || require('./questionMark.png'),
	Frame6_Shapewithtext: tryRequire('./Frame6_Shapewithtext.png') || require('./questionMark.png'),
	Frame5_Shapewithtext: tryRequire('./Frame5_Shapewithtext.png') || require('./questionMark.png'),
	Frame4_Shapewithtext: tryRequire('./Frame4_Shapewithtext.png') || require('./questionMark.png'),
	Frame3_Shapewithtext: tryRequire('./Frame3_Shapewithtext.png') || require('./questionMark.png'),
	Frame1_image1: tryRequire('./Frame1_image1.png') || require('./questionMark.png'),
	Frame1_image2: tryRequire('./Frame1_image2.png') || require('./questionMark.png'),
	Frame6_image8: tryRequire('./Frame6_image8.png') || require('./questionMark.png'),
	Frame5_image7: tryRequire('./Frame5_image7.png') || require('./questionMark.png'),
	Frame4_image6: tryRequire('./Frame4_image6.png') || require('./questionMark.png'),
}