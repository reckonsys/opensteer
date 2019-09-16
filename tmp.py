import pytz
import arrow


'''
<select class="selectpicker" data-live-search="true">
  <option data-tokens="ketchup mustard">Hot Dog, Fries and a Soda</option>
  <option data-tokens="mustard">Burger, Shake and a Smile</option>
  <option data-tokens="frosting">Sugar, Spice and all things nice</option>
</select>
$('select').selectpicker();
'''

utc = arrow.utcnow()
for tz in pytz.all_timezones:
    print(tz, utc.to(tz).format())

'''
'''
