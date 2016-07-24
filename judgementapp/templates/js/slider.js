
function get_labels(left, mid, right){
	var a = [left]
	for (var i=0; i<49; i++) {
		a.push(" ")
	}
	a.push(mid)
	for (var i=0; i<49; i++) {
		a.push(" ")
	}
	a.push(right)
	return a
};



