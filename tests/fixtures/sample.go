package fixture

func persist() string {
	return "stored"
}

func validate() string {
	return persist()
}

func handleRequest() string {
	return validate()
}
