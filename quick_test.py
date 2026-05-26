import captchard.nsut as nsut

print('Loading model...')
model = nsut.load_model('model/final_captcha_model.h5')

image_path = 'captchas/captcha_1750587434.jpg'
print(f'Predicting for: {image_path}')

# Using the new predict alias
prediction = nsut.predict(image_path, model=model)

print('=' * 20)
print(f'Prediction Result: {prediction}')
print('=' * 20)
