<template>
  <v-dialog v-model="shown" scrollable max-width="720">
    <template v-slot:activator="{ on }">
      <v-btn rounded flat outlined v-on="on">
        Click Me
      </v-btn>
    </template>
    <v-card>
      <v-card-actions class="px-6 py-4">
        <v-card-title class="pa-0">{{
          $t("forms.titles.create_customer")
        }}</v-card-title>
        <v-spacer />
        <v-icon @click="shown = false">mdi-close</v-icon>
      </v-card-actions>
      <v-divider></v-divider>
      <v-card-text style="min-height: 300px;padding: 20px 24px 0;">
        <ValidationObserver ref="form">
          <v-form>
            <v-row no-gutters>
              <v-col class="pe-2">
                <label class="font-weight-bold" for="">{{
                  $t("forms.labels.customer.last_name")
                }}</label>
                <TextInput v-model="form.last_name" name="last_name" />
              </v-col>
              <v-col class="pe-6">
                <label class="font-weight-bold" for="">{{
                  $t("forms.labels.customer.first_name")
                }}</label>
                <TextInput v-model="form.first_name" name="first_name" />
              </v-col>
              <v-col class="pe-2">
                <label class="font-weight-bold" for="">セイ</label>
                <TextInput
                  v-model="form.last_name_kana"
                  name="last_name_kana"
                />
              </v-col>
              <v-col>
                <label class="font-weight-bold" for="">メイ</label>
                <TextInput
                  v-model="form.first_name_kana"
                  name="first_name_kana"
                />
              </v-col>
            </v-row>
            <v-row no-gutters>
              <v-col class="pe-6">
                <label class="font-weight-bold" for="">{{
                  $t("forms.labels.customer.postal_code")
                }}</label>
                <TextInput v-model="form.postal_code" name="postal_code" />
              </v-col>
              <v-col>
                <label class="font-weight-bold" for="">{{
                  $t("forms.labels.customer.address")
                }}</label>
                <TextInput v-model="form.address" name="address" />
              </v-col>
            </v-row>
            <v-row no-gutters>
              <v-col class="pe-6">
                <label class="font-weight-bold" for="">{{
                  $t("forms.labels.customer.phone_number")
                }}</label>
                <TextInput name="phone_number" v-model="form.phone_number" />
              </v-col>
              <v-col>
                <label class="font-weight-bold" for="">{{
                  $t("forms.labels.customer.mobile_number")
                }}</label>
                <TextInput name="mobile_phone" v-model="form.mobile_number" />
              </v-col>
            </v-row>
            <v-row no-gutters>
              <v-col class="col-6 pe-3">
                <label class="font-weight-bold" for="">{{
                  $t("forms.labels.customer.email")
                }}</label>
                <TextInput name="email" v-model="form.email" />
              </v-col>
            </v-row>
          </v-form>
        </ValidationObserver>
      </v-card-text>
      <v-divider></v-divider>
      <v-card-actions>
        <v-btn color="blue darken-1" text @click="shown = false">Close</v-btn>
        <v-btn color="blue darken-1" text @click="submit">Save</v-btn>
        <v-spacer />
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import { ValidationObserver, setInteractionMode } from "vee-validate";
import gql from "graphql-tag";
import TextInput from "./forms/TextInput";

setInteractionMode("passive");

export default {
  components: {
    ValidationObserver,
    TextInput,
  },
  data() {
    return {
      shown: false,
      form: {
        first_name: "",
        last_name: "",
        first_name_kana: "",
        last_name_kana: "",
        postal_code: "",
        address: "",
        phone_number: "",
        mobile_number: "",
        email: "",
      },
    };
  },
  methods: {
    submit() {
      this.$apollo.matate({
        mutation: gql`
          createCustomer ($input: CreateCustomerInput!) {
            create_customer(data: $input) {
              ok
              error
              customer {
                id
              }
            }
        }`,
        variables: {
          input: {
            name: {
              last_name: this.data.form.last_name,
              first_name: this.data.form.first_name,
              last_name_kana: this.data.form.last_name_kana,
              first_name_kana: this.data.form.first_name_kana,
            },
            address: {
              prefecture: this.data.form.address,
            },
            contact: {
              postal_code: this.data.form.postal_code,
              telephone: this.data.form.phone_number,
              mobilephone: this.data.form.mobile_number,
              email: this.data.form.email,
            },
          },
        },
        update: (store, { data: { ok, error } }) => {
          if (!ok) {
            this.$refs.form.setErrors(error);
          } else {
            this.$apollo.queries.list_customers.start();
          }
        },
      });
    },
  },
};
</script>
